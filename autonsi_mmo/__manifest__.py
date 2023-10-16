# Part of Softhealer Technologies.
{
    'name': 'Auto&S.I MMO',
    "author": "Auto&S.I",
    "website": "https://www.autonsi.com",
    "support": "s",
    "category": "Stock",
    "license": "OPL-1",
    "summary": "Implement MMO for Odoo",
    "description": """Implement MMO for Odoo""",
    "version": "15.0.1",
    'depends': [
                'mrp',
                'stock',
                'purchase',
                'sale',
                'l10n_vn',
    ],
    'data': [
        'views/product.xml',
        'views/menu.xml',
        'security/ir.model.access.csv'
              ],
    "images": ["static/description/background.png", ],
    "auto_install": False,
    "installable": True,
}
