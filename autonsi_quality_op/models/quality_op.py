from odoo import api, fields, models


class QualityOP(models.Model):
    _inherit = 'sh.mrp.quality.check'

    product_picking_id = fields.Many2one('product.product', string='Product', related="stock_move_id.product_id")
    product_picking_qty = fields.Float("Quantity",related="stock_move_id.product_uom_qty")
    stock_picking_id = fields.Many2one('stock.picking')
    stock_move_id = fields.Many2one('stock.move')
    qc_sop_picking_type = fields.Many2one('autonsi.quality.qcsoptype', "QC SOP Type")



