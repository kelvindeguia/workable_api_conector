# -*- coding: utf-8 -*-
import requests
import logging
import time
from datetime import datetime

from odoo import models, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

WORKABLE_API_BASE = "https://{subdomain}.workable.com/spi/v3"


class WorkableHiringPlanSync(models.Model):
    _inherit = 'workable.hiring.plan'

    # -------------------------------
    # Credentials
    # -------------------------------
    def _get_workable_credentials(self):
        ICP = self.env['ir.config_parameter'].sudo()
        token = ICP.get_param('workable.api_token')
        subdomain = ICP.get_param('workable.subdomain')

        if not token or not subdomain:
            raise UserError(
                'Workable API Token or Subdomain is not configured. '
                'Go to Settings > General Settings > Workable Integration.'
            )

        return token.strip(), subdomain.strip()

    # -------------------------------
    # Safe Request with Retry
    # -------------------------------
    def _safe_request(self, url, headers, params=None):
        max_retries = 5
        retry_delay = 2  # seconds

        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers, params=params, timeout=30)

                # Handle rate limit
                if response.status_code == 429:
                    _logger.warning(
                        "Workable rate limit hit. Retrying in %s seconds (attempt %s/%s)",
                        retry_delay, attempt + 1, max_retries
                    )
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue

                response.raise_for_status()
                return response

            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    raise UserError(f"Failed to connect to Workable: {str(e)}")
                time.sleep(retry_delay)
                retry_delay *= 2

        raise UserError("Max retries exceeded due to rate limiting.")

    # -------------------------------
    # Fetch Requisitions (Optimized)
    # -------------------------------
    def _fetch_workable_requisitions(self):
        token, subdomain = self._get_workable_credentials()

        base_url = WORKABLE_API_BASE.format(subdomain=subdomain)
        url = f"{base_url}/requisitions"

        headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json',
        }

        # Get last sync (optional incremental support)
        ICP = self.env['ir.config_parameter'].sudo()
        last_sync = ICP.get_param('workable.last_sync')

        params = {
            'limit': 100,  # MAX allowed → fewer requests
        }

        # OPTIONAL incremental (enable if supported by API)
        # if last_sync:
        #     params['updated_after'] = last_sync

        requisitions = []
        first_call = True
        page = 1

        while url:
            _logger.info("Fetching Workable page %s", page)

            response = self._safe_request(
                url,
                headers,
                params=params if first_call else None
            )

            first_call = False

            try:
                data = response.json()
            except Exception:
                raise UserError(f"Invalid JSON response: {response.text}")

            page_reqs = data.get('requisitions', [])
            requisitions.extend(page_reqs)

            _logger.info("Fetched %s records (total so far: %s)", len(page_reqs), len(requisitions))

            # Pagination
            url = data.get('paging', {}).get('next')

            page += 1

            # Respect rate limit
            if url:
                time.sleep(2)

        # Save last sync timestamp
        ICP.set_param('workable.last_sync', datetime.utcnow().isoformat())

        return requisitions

    # -------------------------------
    # Mapping
    # -------------------------------
    def _map_requisition(self, req):
        job = req.get('job', {})
        department = req.get('department', {})
        location = req.get('location', {})
        hiring_manager = req.get('hiring_manager', {})
        owner = req.get('owner', {})
        requester = req.get('requester', {})
        salary = req.get('salary_range', {})

        calibration_notes_url = None
        for attr in req.get('requisition_attributes', []):
            if attr.get('name') == 'Calibration Notes':
                calibration_notes_url = (attr.get('value') or {}).get('preview_url')
                break

        employment_type_map = {
            'Full-time': 'full_time',
            'Part-time': 'part_time',
            'Contract': 'contract',
            'Temporary': 'temporary',
        }

        reason_map = {
            'new_hire': 'new_hire',
            'replacement': 'replacement',
            'backfill': 'backfill',
        }

        approved_by = ', '.join([
            approver.get('name', '')
            for group in req.get('approval_groups', [])
            for approver in group.get('approvers', [])
            if approver.get('decision') == 'approved'
        ])

        return {
            'requisition_id': req.get('code', ''),
            'workable_requisition_id': req.get('id', ''),
            'job_title': job.get('title', ''),
            'workable_job_id': job.get('id', ''),
            'workable_shortcode': job.get('shortcode', ''),
            'department': department.get('name', ''),
            'workable_department_id': department.get('id', ''),
            'requisition_location': location.get('location_str', ''),
            'hiring_manager': hiring_manager.get('name', ''),
            'requisition_owner': owner.get('name', ''),
            'requestor': requester.get('name', ''),
            'plan_date': req.get('plan_date') or False,
            'target_start_date': req.get('start_date') or False,
            'employment_type': employment_type_map.get(req.get('employment_type'), 'full_time'),
            'reason': reason_map.get(req.get('reason'), 'new_hire'),
            'salary_from': salary.get('from') or 0.0,
            'salary_to': salary.get('to') or 0.0,
            'salary_currency': salary.get('currency', ''),
            'salary_frequency': salary.get('frequency', ''),
            'calibration_notes_url': calibration_notes_url,
            'approved_by': approved_by,
            'status': 'open' if req.get('state') in ('open', 'approved') else 'closed',
        }

    # -------------------------------
    # Create / Update
    # -------------------------------
    def _process_requisitions(self, requisitions):
        created = updated_records = field_changes = 0
        changed_fields = []

        for req in requisitions:
            req_code = req.get('id')
            if not req_code:
                continue

            vals = self._map_requisition(req)

            existing = self.search(
                [('workable_requisition_id', '=', req_code)],
                limit=1
            )

            if existing:
                changes_count, fields_list = self._count_changes(existing, vals)
                if changes_count > 0:
                    existing.write(vals)
                    updated_records += 1
                    field_changes += changes_count
                    changed_fields.extend(fields_list)
            else:
                self.create(vals)
                created += 1

        unique_fields = list(set(changed_fields))

        _logger.info(
            'Workable employees sync: %d created, %d records updated (%d fields modified: %s)',
            created, updated_records, field_changes,
            ', '.join(unique_fields) if unique_fields else 'none'
        )

        return created, updated_records, field_changes, unique_fields

    # -------------------------------
    # Check for Changes
    # -------------------------------
    def _count_changes(self, record, new_vals):
        fields_to_check = list(new_vals.keys())
        current_vals = record.read(fields_to_check)[0]

        changes = 0
        changed_fields = []

        for field, new_value in new_vals.items():
            current_value = current_vals.get(field)

            current_value = self._normalize_value(current_value)
            new_value = self._normalize_value(new_value)

            if current_value != new_value and not (
                current_value in (False, None) and new_value in (False, None, '')
            ):
                changes += 1
                changed_fields.append(field)

        return changes, changed_fields
    
    # -------------------------------
    # Normalize
    # -------------------------------
    def _normalize_value(self, value):
        if isinstance(value, str):
            return value.strip()
        elif hasattr(value, 'strftime'):
            return value.strftime('%Y-%m-%d')
        elif isinstance(value, float):
            return round(value, 6)
        return value

    # -------------------------------
    # Manual Sync
    # -------------------------------
    def action_sync_from_workable(self):
        try:
            requisitions = self._fetch_workable_requisitions()
            created, updated_records, field_changes, _ = self._process_requisitions(requisitions)

            return {
                    "params": {
                        "title": "Workable Sync",
                        "message": "Sync Done: %s created, %s updated (%s field changes)" % (
                            created, updated_records, field_changes,
                        ),
                        "type": "success",
                    }
                }
        except UserError as e:
            # Optional: also log
            _logger.error("Workable requisitions sync failed: %s", e)
            return {
                "params": {
                    "title": _("Workable Sync Error"),
                    "message": str(e),
                    "type": "danger",
                }
            }

    # -------------------------------
    # Cron
    # -------------------------------
    @api.model
    def cron_sync_from_workable(self):
        try:
            requisitions = self._fetch_workable_requisitions()
            created, updated_records, field_changes, _ = self._process_requisitions(requisitions)
            
            _logger.info(
                'Cron Sync Done: %s created, %s updated (%s field changes)',
                created, updated_records, field_changes
            )
        
        except UserError as e:
            _logger.error('Workable requisition cron sync failed: %s', str(e))