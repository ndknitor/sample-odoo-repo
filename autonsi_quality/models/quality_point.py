# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class ShQcPoint(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'sh.qc.point'
    _description = "Quality Point"

    product_id = fields.Many2one("product.product", "Product")
    type_id = fields.Boolean(string="Type Id")
    logged_user = fields.Many2one(
        'res.users', 'Responsible', readonly=True, default=lambda self: self.env.user)
    company_id = fields.Many2one(
        'res.company', string="Company", default=lambda self: self.env.company)
    name = fields.Char(string="QC SOP Title")
    operation = fields.Many2one("stock.picking.type", "Picking Type")
    team = fields.Many2one("sh.qc.team", "Team", default=1)
    sh_message = fields.Text("Message if Fail")
    sh_instruction = fields.Text("Instruction")
    type = fields.Selection([('type1', 'Pass Fail'), ('type2', 'Measurement'),
                             ('type3', 'Take a Picture'), ('type4', 'Text'), ('type5', 'QC SOP')], 'Type')
    qc_sop_categories = fields.Selection([('iqc', 'IQC'), ('pqc', 'PQC'),
                                          ('oqc', 'OQC')], 'QC SOP Category')
    qc_sop_form_id = fields.Many2one('mes.qc_form', 'QC SOP Form')
    qc_sop_type_iqc = fields.Selection([('raw_material', 'Raw Material'), ('material', 'Material')], 'QC SOP Type')
    qc_sop_type_pqc = fields.Selection([('after_setting', 'After Setting'), ('semi_lot', 'SEMI LOT')], 'QC SOP Type')
    qc_sop_type_oqc = fields.Selection([('after_qc', 'After QC'), ('after_packing', 'After Packing')], 'QC SOP Type')
    qc_sop_type = fields.Many2one('autonsi.quality.qcsoptype')
    sh_norm = fields.Float("Norm")
    sh_unit_to = fields.Float("To")
    sh_unit_from = fields.Float("From")
    sh_signature = fields.Text(string="")
    is_mandatory = fields.Boolean("QC Mandatory ?")
    number_of_test = fields.Integer(
        "Maximum number of tests allowed.", default=1)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('sh.qc.point')
        return super(ShQcPoint, self).create(vals)

    @api.onchange('type')
    def _onchange_marital(self):
        if self.type and self.type == "type2":
            self.type_id = True
        else:
            self.type_id = False

    @api.onchange('qc_sop_type_iqc')
    def _onchange_qc_sop_type_iqc(self):
        if self.qc_sop_type_iqc == "raw_material":
            self.qc_sop_type = "Raw Material"
        if self.qc_sop_type_iqc == "material":
            self.qc_sop_type = "Material"

    @api.onchange('qc_sop_type_oqc')
    def _onchange_qc_sop_type_oqc(self):
        if self.qc_sop_type_oqc == "after_qc":
            self.qc_sop_type = "After QC"
        if self.qc_sop_type_oqc == "after_packing":
            self.qc_sop_type = "After Packing"

    @api.onchange('qc_sop_type_pqc')
    def _onchange_qc_sop_type_pqc(self):
        if self.qc_sop_type_pqc == "after_setting":
            self.qc_sop_type = "After Setting"
        if self.qc_sop_type_pqc == "semi_lot":
            self.qc_sop_type = "SEMI LOT"


    def get_read_data(self, id=None, min_date=None, max_date=None):
        print("Pop up")
        print(id)
        print(min_date)
        print(max_date)
