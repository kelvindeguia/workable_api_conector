# -*- coding: utf-8 -*-
from odoo import models, fields, api

class WorkableJob(models.Model):
    _name = 'workable.job'
    _description = 'Workable Job'
    _order = 'id'
    _rec_name = 'job_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Internal / Display Identifier
    job_id = fields.Char(string='Job ID', required=True, store=True)
    # Job Fields
    title = fields.Char(string='Title', store=True)
    full_title = fields.Char(string='Full Title', store=True)
    shortcode = fields.Char(string='Shortcode', store=True)
    code = fields.Char(string='Job Code', store=True)
    state = fields.Selection([('draft', 'Draft'), ('published', 'Published'), ('closed', 'Closed'), ('archived', 'Archived'),], string='State', store=True)
    confidential = fields.Boolean(string='Confidential', store=True)
    # Department
    department_id = fields.Char(string='Department', store=True)
    department_hierarchy_id = fields.Text(string='Department Hierarchy', store=True)
    # URLs
    url = fields.Char(string='URL', store=True)
    application_url = fields.Char(string='Application URL', store=True)
    shortlink = fields.Char(string='Short Link', store=True)
    # Workplace / Location Summary
    workplace_type = fields.Selection([('on_site', 'On Site'), ('hybrid', 'Hybrid'), ('remote', 'Remote'),], string='Workplace Type', store=True)
    job_location = fields.Char(string='Location', store=True)
    # location_str = fields.Char(string='Location', store=True)
    # country = fields.Char(string='Country', store=True)
    # country_code = fields.Char(string='Country Code', store=True)
    # region = fields.Char(string='Region', store=True)
    # region_code = fields.Char(string='Region Code', store=True)
    # city = fields.Char( string='City', store=True)
    # zip_code = fields.Char( string='ZIP Code', store=True)
    # telecommuting = fields.Boolean(string='Telecommuting', store=True)
    # Salary
    salary_currency = fields.Char(string='Salary Currency', store=True)
    # Dates
    created_at = fields.Datetime(string='Created At', tracking=True, store=True)
    updated_at = fields.Datetime(string='Updated At', tracking=True, store=True)
    # Other Metadata
    keywords = fields.Char(string='Keywords', store=True)
    # External Identifiers
    workable_job_id = fields.Char(string='Workable Job ID', store=True)