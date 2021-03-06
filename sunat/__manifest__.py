# -*- coding: utf-8 -*-
{
    'name': "Sunat Peru",

    'summary': """
        Los procesos que pide sunat el la contabilidad""",

    'description': """
        Se toca temas como la detraccion y la retencion
    """,

    'author': "Optimiza",
    'website': "http://grupooptimiza.la",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'sequence':0,
    'category': 'Generic Modules/Base',
    'application': True,
    'version': '1.2',
    'installable': True,
    'auto_install': True,

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/detraccion.xml',
        'views/document_type.xml',
        'views/currency_type.xml',
        'views/customs_code.xml',
        'views/classification_goods.xml',
        'views/document_type_identity.xml',
        'views/views.xml',
        'views/templates.xml',
        'wizard/account_bill_txt_view.xml',
        'views/menu.xml',
        'data/data_detracciones.xml',
        'data/currency_type.xml',
        'data/customs_code.xml',
        'data/classification_goods.xml',
        'data/document_type.xml',
        'data/document_type_identity.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}