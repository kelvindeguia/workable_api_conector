# -*- coding: utf-8 -*-
{
    'name': 'Workable Job Integration',
    'version': '18.0.0.0.0',
    'category': 'Workable/Jobs',
    'summary': 'API Integration with Workable Jobs for Odoo',
    'description': """
        Workable Jobs API Integration for Odoo
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
        'views/workable_job_views.xml',
        'views/menuitems.xml',
    ],
    'assets': {
        'web.assets_backend': [
                'workable_job/static/src/js/sync_button.js',
                'workable_job/static/src/xml/sync_button.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}