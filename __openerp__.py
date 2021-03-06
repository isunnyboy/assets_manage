# -*- coding: utf-8 -*-
{
    'name': "Assets_manage",

    # 'summary': """
    #     Short (1 phrase/line) summary of the module's purpose, used as
    #     subtitle on modules listing or apps.openerp.com""",

    'description': """
    """,

    'author': "Your Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'assetsmanagement',
    # 'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/resource_security.xml',
        'security/ir.model.access.csv',
        # 'templates.xml',
        'views/assets_management_newRequest.xml',
        'views/assets_management_view.xml',
        'views/assets_management_menu.xml',
        'views/assets_management_link.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
    'application': True,
    'qweb': [
        'static/src/xml/assets_manage.xml',
    ],
}