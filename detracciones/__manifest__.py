# -*- coding: utf-8 -*-
{
    'name': "Sunat Detracciones",

    'summary': """
        Listado de los codigos de las detracciones""",

    'description': """
        Es una tabla maestra que sirve a las demas
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Generic Modules/Base',
    'application': True,
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/tipo_doc.xml',
        'views/bill.xml',
        'security/ir.model.access.csv',
        'data/data_detracciones.xml',
        'data/data_document_type.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}