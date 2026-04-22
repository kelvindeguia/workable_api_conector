from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    workable_api_token = fields.Char(
        string='Workable API Token',
        config_parameter='workable.api_token'
    )
    workable_subdomain = fields.Char(
        string='Workable Subdomain',
        help='Your Workable account subdomain, e.g. "mycompany" from mycompany.workable.com',
        config_parameter='workable.subdomain'
    )