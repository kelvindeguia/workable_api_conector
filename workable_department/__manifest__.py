# -*- coding: utf-8 -*-
{
    'name': 'Workable Department Integration',
    'version': '18.0.0.0.0',
    'category': 'Workable/Departments',
    'summary': 'API Integration with Workable Departments for Odoo',
    'description': """
        Workable Departments API Integration for Odoo
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
        'views/workable_department_views.xml',
        'views/menuitems.xml',
    ],
    'assets': {
        'web.assets_backend': [
                'workable_department/static/src/js/sync_button.js',
                'workable_department/static/src/xml/sync_button.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}