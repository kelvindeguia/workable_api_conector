# -*- coding: utf-8 -*-
{
    'name': 'Workable Employee Integration',
    'version': '18.0.0.0.0',
    'category': 'Workable/Employees',
    'summary': 'API Integration with Workable Onboarding/Employees for Odoo',
    'description': """
        Workable Employees API Integration for Odoo
    """,
    'author': 'Module Author',
    'depends': [
        'base',
        'mail',
        'hr',
        'hr_recruitment',
        'workable_connector',
    ],
    'data': [
        # Security
        'security/security_views.xml',
        'security/ir.model.access.csv',
        # Views
        'views/workable_employee_views.xml',
        'views/menuitems.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'workable_employee/static/src/js/sync_button.js',
            'workable_employee/static/src/xml/sync_button.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

