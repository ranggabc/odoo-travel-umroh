# -*- coding: utf-8 -*-
{
    'name': "Travel Umroh",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Rangga Bayu C",
    'website': "http://www.rangga.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'mrp', 'sale', 'report_xlsx'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/sequence_data.xml',
        'views/views.xml',
        'views/package_views.xml',
        'report/report_action.xml',
        'report/report_delivery_order.xml',
        'report/report_payment_move.xml',
        'views/menuitem_views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}
