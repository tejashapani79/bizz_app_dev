# -*- coding: utf-8 -*-
{
    'name': "BizzAppDev Tejas Apani",

    'summary': "BizzAppDev Tejas Apani",

    'description': """
BizzAppDev Tejas Apani
    """,

    'author': "Tejas Apani",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'contacts', 'stock', 'sale_management', 'mrp','purchase'],

    'data': [
        'views/stock_picking_view.xml',
        'views/sale_order_view.xml'

    ],
    "assets": {
        "web.assets_backend": [
            "bad_tejas_apani/static/src/js/clipboard_field.js",
            "bad_tejas_apani/static/src/xml/clipboard_field.xml"
        ]
    },

}
