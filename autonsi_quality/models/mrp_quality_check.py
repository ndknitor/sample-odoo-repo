# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import SUPERUSER_ID, _, api, fields, models, registry
from odoo.exceptions import ValidationError

class QCSOPType(models.Model):
    _name = "autonsi.quality.qcsoptype"
    _description = 'QC SOP Type'

    qc_sop_category = fields.Selection([('iqc', 'IQC'), ('pqc', 'PQC'), ('oqc', 'OQC')],
                                       default=False, string="QC SOP Category")
    name = fields.Char("QC SOP Type")
    description_text = fields.Text("Description")

    @api.constrains('qc_sop_category', 'name')
    def constrain_name_apply(self):
        record = self.env['autonsi.quality.qcsoptype'].search([('name', '=', self.name), ('qc_sop_category', '=', self.qc_sop_category)])
        if len(record) > 1:
            raise ValidationError('The type with the same QC SOP Type and QC SOP Category has already existed')


class ShMrpQualityCheck(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'sh.mrp.quality.check'
    _description = "MRP Quality Check"
    _rec_name = 'product_id'

    product_id = fields.Many2one("product.product", "Product", related="sh_mrp.product_id")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pass', 'Pass'),
        ('fail', 'Fail')
    ], string='Status', readonly=True, index=True, copy=False, default='draft')
    product_qty = fields.Float(string="Qty", related="sh_mrp.product_qty")
    sh_workorder_id = fields.Many2one('mrp.workorder', 'Work Order')
    sh_mrp = fields.Many2one("mrp.production", string="Reference")
    sh_date = fields.Date("Date")
    sh_control_point = fields.Char(string="Control Point ")
    control_point_id = fields.Many2one("sh.qc.point", string="Control Point")
    sh_norm = fields.Float("Measure")
    qc_type = fields.Selection([('type1', 'Pass Fail'), ('type2', 'Measurement'), (
        'type3', 'Take A picture'), ('type4', 'Text'), ('type5', 'QC SOP')], 'Type')
    company_id = fields.Many2one(
        'res.company', 'Company', default=lambda self: self.env.company)
    attachment_ids = fields.Many2many('ir.attachment', string="QC pictures")
    text_message = fields.Text("QC Text")
    qc_sop_categories = fields.Selection([('iqc', 'IQC'), ('pqc', 'PQC'), ('oqc', 'OQC'), ('app', 'APP')],
                                         related="qc_sop_type.qc_sop_category", string="QC SOP Category")
    mes_qc_form_id = fields.Many2one('mes.qc_form', default=False, string='QC SOP')
    qc_sop_type_iqc = fields.Selection([('raw_material', 'Raw Material'), ('material', 'Material')], 'QC SOP Type')
    qc_sop_type_pqc = fields.Selection([('after_setting', 'After Setting'), ('semi_lot', 'SEMI LOT')], 'QC SOP Type')
    qc_sop_type_oqc = fields.Selection([('after_qc', 'After QC'), ('after_packing', 'After Packing')], 'QC SOP Type')
    qc_sop_type = fields.Many2one('autonsi.quality.qcsoptype', 'QC SOP Type')
    mmo_id = fields.Many2one('mrp.masterproduction', string='Master Manufacturing')
    operation_name = fields.Char('Operation Name', related="sh_mrp.operation_name")

    def accept(self):
        self.write({'state': 'pass'})

    def reject(self):
        self.write({'state': 'fail'})

    @api.onchange('qc_sop_categories')
    def _onchange(self):
        print(self.qc_sop_categories)

    def plan_get_item_view(self):
        viewid = 'autonsi_quality.qualitycheckview'
        viewidname = self.env.ref(viewid).id
        return viewidname

    @api.onchange('qc_sop_type_iqc')
    def _onchange_qc_sop_type_iqc(self):
        if self.qc_sop_type_iqc == "raw_material":
            self.qc_sop_type = "Raw Material"
        if self.qc_sop_type_iqc == "material":
            self.qc_sop_type = "Material"
        self.qc_sop_categories = 'iqc'

    @api.onchange('qc_sop_type_oqc')
    def _onchange_qc_sop_type_oqc(self):
        if self.qc_sop_type_oqc == "after_qc":
            self.qc_sop_type = "After QC"
        if self.qc_sop_type_oqc == "after_packing":
            self.qc_sop_type = "After Packing"
        self.qc_sop_categories = 'oqc'
    @api.onchange('qc_sop_type_pqc')
    def _onchange_qc_sop_type_pqc(self):
        if self.qc_sop_type_pqc == "after_setting":
            self.qc_sop_type = "After Setting"
        if self.qc_sop_type_pqc == "semi_lot":
            self.qc_sop_type = "SEMI LOT"
        self.qc_sop_categories = 'pqc'

    @api.onchange('qc_sop_type')
    def _onchange_qc_sop_type(self):
        self.qc_sop_categories = 'pqc'

    def compute_qc_sop_type(self):
        for line in self:
            if line.qc_sop_categories == "iqc":
                if line.qc_sop_type_iqc == "raw_material":
                    line.qc_sop_type = "Raw Material"
                if line.qc_sop_type_iqc == "material":
                    line.qc_sop_type = "Material"
            elif line.qc_sop_categories == "oqc":
                if line.qc_sop_type_oqc == "after_qc":
                    line.qc_sop_type = "After QC"
                if line.qc_sop_type_oqc == "after_packing":
                    line.qc_sop_type = "After Packing"
            elif line.qc_sop_categories == "pqc":
                if line.qc_sop_type_pqc == "after_setting":
                    line.qc_sop_type = "After Setting"
                if line.qc_sop_type_pqc == "semi_lot":
                    line.qc_sop_type = "SEMI LOT"
            print(line.qc_sop_type)
