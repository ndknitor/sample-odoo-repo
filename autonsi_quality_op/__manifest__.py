# Part of Softhealer Technologies.
{
    'name': 'Auto&S.I Quality OP',
    "author": "Auto&S.I",
    "website": "https://www.autonsi.com",
    "support": "s",
    "category": "Stock",
    "license": "OPL-1",
    "summary": "Quality OP",
    "description": """Quality OP""",
    "version": "15.0.1",
    'depends': [
        'autonsi_process',
        'autonsi_quality',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking_view.xml',
        'wizard/mes_qc_list_popup.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'autonsi_quality/static/lib/codebase/suite.css',
            'autonsi_quality/static/lib/codebase/suite.js',
            'autonsi_quality_op/static/src/js/widget_qc_list.js',
        ],

        'web.assets_qweb': {
            'autonsi_quality_op/static/src/xml/mes_qc_list_template.xml',
        },
    },
    "auto_install": True,
    "installable": True,
}
