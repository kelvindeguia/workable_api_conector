# -*- coding: utf-8 -*-
from odoo import models, fields, api


class WorkableCandidate(models.Model):
    _name = 'workable.candidate'
    _description = 'Workable Candidate'
    _order = 'id'
    _rec_name = 'name'

    name = fields.Char(string='Candidate Name', required=True, store=True)