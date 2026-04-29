# -*- coding: utf-8 -*-
from odoo import models, fields, api

class WorkableDepartment(models.Model):
    _name = 'workable.department'
    _description = 'Workable Department'
    _order = 'id'
    _rec_name = 'department_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    department_id = fields.Char(string='Department ID', required=True, store=True)
    name = fields.Char(string='Name', store=True)
    parent_id = fields.Char(string='Parent ID', store=True)
    sample = fields.Char(string='Sample', store=True)

