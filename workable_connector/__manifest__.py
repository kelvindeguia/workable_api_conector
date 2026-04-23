# -*- coding: utf-8 -*-
{
    'name': 'Workable Integration',
    'version': '18.0.0.0.0',
    'category': 'Workable/Connector',
    'summary': 'API Integration with Workable for Odoo',
    'icon': 'static/description/workable_icon.png',
    'description': """
        Workable ATS API Integration for Odoo
    """,
    'author': 'Kelvin De Guia',
    'depends': [
        'base',
        'mail',
        'hr',
        'hr_recruitment',
    ],
    'data': [
        # Security
        'security/security_views.xml',
        'security/ir.model.access.csv',
        # Views
        'views/hiring_plan_views.xml',
        'views/res_config_settings_views.xml',
        'views/menuitems.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'workable_connector/static/src/js/sync_button.js',
            'workable_connector/static/src/xml/sync_button.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
