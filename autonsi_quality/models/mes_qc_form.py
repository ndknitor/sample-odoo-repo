# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = "product.product"

    mes_qc_form_id = fields.Many2one('mes.qc_form', string='MES QC Form')


class Manufacturing(models.Model):
    _inherit = 'mrp.production'
    mes_qc_form_id = fields.Many2one('mes.qc_form', string='MES QC Form')


class MESQCFormQuestion(models.Model):
    _name = "mes.qc_form_questions"
    _description = "MES QC Form Question"

    question_type = fields.Selection([
        ('matrix', 'Matrix'),
        ('raw_material', 'Raw Material'),
        ('material', 'Material')], string='Question Type',
        compute='_compute_question_type', readonly=False, store=True)
    title = fields.Char(string='Question Title')
    qc_form_id = fields.Many2one('mes.qc_form', string="Form ID")
    answers_ids = fields.One2many('mes.qc_form_answers', 'qc_form_question_id', string="Answers")
    matrix_row_ids = fields.One2many('mes.qc_form_answers', 'qc_form_question_id', string="Matrix Rows")
    mes_qc_type_ids = fields.Many2one('mes.qc_type', string="QC Type")
    mes_qc_item_ids = fields.Many2one('mes.qc_item', string="QC Item")
    mes_qc_standard_ids = fields.Many2one('mes.qc_standard', string="QC Standard")
    mes_qc_tool_ids = fields.Many2one('mes.qc_tool', string="QC Tool")
    mes_qc_frequency_ids = fields.Many2one('mes.qc_frequency', string="QC Frequency")
    n_values = fields.Integer('N Values')
    units = fields.Many2one('uom.uom', string="Unit")


class MESQCFormAnswers(models.Model):
    _name = "mes.qc_form_answers"
    _description = "MES QC Form Answer"

    value = fields.Char(string='Answer Value')
    question_key = fields.Char(string='Question Key')
    qc_form_question_id = fields.Many2one('mes.qc_form_questions', string="Question ID")
    qc_form_id = fields.Many2one('mes.qc_form', string="QC SOP")


class MESQCAnswersRecord(models.Model):
    _name = "mes.qc_form_answers_record"
    _description = "MES QC Form Answer Record"

    value = fields.Char(string='Answer Value')
    question_key = fields.Char(string='Question Key')
    qc_answers_id = fields.Many2one('mes.qc_answers', string="Answer ID")


class MESQCAnswers(models.Model):
    _name = "mes.qc_answers"
    _description = "MES QC Answer"

    answer_record_ids = fields.One2many('mes.qc_form_answers_record', 'qc_answers_id', string='Answers')
    qc_id = fields.Many2one('sh.mrp.quality.check', string="Quality Check ID")


class ShMrpQualityCheck(models.Model):
    _inherit = 'sh.mrp.quality.check'
    mes_qc_answers = fields.One2many('mes.qc_answers', 'qc_id', string='MES QC Answer')


class MESQCForm(models.Model):
    _name = "mes.qc_form"
    _description = "MES QC Form"

    name = fields.Char(string='QC SOP Title', required=True)
    question_ids = fields.One2many('mes.qc_form_questions', 'qc_form_id', 'Question List')
    product_id = fields.Many2one('product.product')
    qc_sop_category = fields.Selection([('iqc', 'IQC'), ('pqc', 'PQC'), ('oqc', 'OQC')],
                                       default=False, string="QC SOP Category")

    qc_sop_type = fields.Many2one('autonsi.quality.qcsoptype')
    qc_sop_type_text = fields.Char(string="QC SOP Type text", related="qc_sop_type.name")
    operation_name = fields.Char(string='Operation Name')

    answers_ids = fields.One2many('mes.qc_form_answers', 'qc_form_question_id', string="Answers")
    matrix_row_ids = fields.One2many('mes.qc_form_answers', 'qc_form_question_id', string="Matrix Rows")
    mes_qc_type_ids = fields.Many2one('mes.qc_type', string="QC Type")
    mes_qc_item_ids = fields.Many2one('mes.qc_item', string="QC Item")
    mes_qc_standard_ids = fields.Many2one('mes.qc_standard', string="QC Standard")
    mes_qc_tool_ids = fields.Many2one('mes.qc_tool', string="QC Tool")
    mes_qc_frequency_ids = fields.Many2one('mes.qc_frequency', string="QC Frequency")
    n_values = fields.Integer('N Values')
    units = fields.Many2one('uom.uom', string="Unit")

    def preview_qc_form(self):

        sname = 'Quality Checks Popup'
        viewid = 'autonsi_quality.sh_mr_quality_check_wizard_form_view'
        viewidname = self.env.ref(viewid).id
        defaultquestion_ids = []
        question_context = []
        print(self.question_ids)
        for question in self.question_ids:
            defaultquestion_ids.append(question)
        context_data = {
            'form_id': self.id,
            'question_id': question_context,
            'default_question_ids': defaultquestion_ids,
            'view_mode': "QC SOP Preview"
        }
        for type in self.qc_sop_type:
            question = self
            append_object = {'qc_sop_type': type.name}
            question_context.append(append_object)
            if type.name == "Matrix":
                answer_ids = []
                matrix_row_ids = []
                matrix_data = {}
                for answer in question.answers_ids:
                    print(answer.value)
                    answer_ids.append(answer.value)
                for matrix_row in question.matrix_row_ids:
                    matrix_row_ids.append(matrix_row.value)
                matrix_data['answer_ids'] = answer_ids
                matrix_data['matrix_rows_ids'] = matrix_row_ids
                context_data['matrix_data'] = matrix_data
            if type.name == 'Raw Material':
                print(question)
                raw_material = {}
                raw_material['mes_qc_type'] = question.mes_qc_type_ids.name
                raw_material['mes_qc_item'] = question.mes_qc_item_ids.name
                raw_material['n_values'] = question.n_values
                raw_material['units'] = question.units.name
                context_data['raw_material'] = raw_material
            if type.name == 'Material':
                material_data = {}
                material_data['mes_qc_type'] = question.mes_qc_type_ids.name
                material_data['mes_qc_item'] = question.mes_qc_item_ids.name
                material_data['mes_qc_standard'] = question.mes_qc_standard_ids.name
                material_data['mes_qc_tool'] = question.mes_qc_tool_ids.name
                material_data['mes_qc_frequency'] = question.mes_qc_frequency_ids.name
                context_data['material_data'] = material_data
            if type.name == 'After Setting' or type.name == 'SEMI LOT':
                after_setting_data = {}
                after_setting_data['mes_qc_type'] = question.mes_qc_type_ids.name
                after_setting_data['mes_qc_item'] = question.mes_qc_item_ids.name
                after_setting_data['mes_qc_standard'] = question.mes_qc_standard_ids.name
                after_setting_data['mes_qc_tool'] = question.mes_qc_tool_ids.name
                after_setting_data['mes_qc_frequency'] = question.mes_qc_frequency_ids.name
                context_data['pqc_data'] = after_setting_data
            if type.name == 'After QC':
                oqc_data = {}
                oqc_data['mes_qc_type'] = question.mes_qc_type_ids.name
                oqc_data['mes_qc_item'] = question.mes_qc_item_ids.name
                oqc_data['mes_qc_standard'] = question.mes_qc_standard_ids.name
                oqc_data['mes_qc_tool'] = question.mes_qc_tool_ids.name
                oqc_data['mes_qc_frequency'] = question.mes_qc_frequency_ids.name
                context_data['oqc_data'] = oqc_data
        print(context_data)
        return {
            'name': sname,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mes.qualitycheckpopup',
            'context': context_data,
            'type': 'ir.actions.act_window',
            'target': 'new'
        }


class MESQCType(models.Model):
    _name = "mes.qc_type"
    _description = "MES QC Type"

    name = fields.Char(string='Name')
    apply = fields.Selection([('iqc', 'IQC'), ('pqc', 'PQC'), ('oqc', 'OQC'), ('mold', 'MOLD'), ('app', 'APP')],
                             string="Apply")
    user_created_id = fields.Many2one('res.partner', string='User Created')
    create_date = fields.Date('Create Date')
    user_updated_id = fields.Many2one('res.partner', string='User Updated')
    update_date = fields.Date('Update Date')
    qc_form_question_id = fields.Many2one('mes.qc_form_questions', string='MES QC Form')

    @api.constrains('name', 'apply')
    def constrain_name_apply(self):
        record = self.env['mes.qc_type'].sudo().search(['&', ('name', '=', self.name), ('apply', '=', self.apply)])
        if len(record) > 1:
            raise ValidationError('The type with the same Name and Apply has already existed')


class MESQCItem(models.Model):
    _name = "mes.qc_item"
    _description = "MES QC Item"

    qc_type_id = fields.Many2one('mes.qc_type', string="Type")
    name = fields.Char(string='Name')
    apply = fields.Selection([('iqc', 'IQC'), ('pqc', 'PQC'), ('oqc', 'OQC'), ('mold', 'MOLD'), ('app', 'APP')],
                             string="Apply")

    display_name = fields.Char(string='Display Name', compute='compute_display_name')

    def compute_display_name(self):
        for item in self:
            if item.qc_type_id.name != False:
                item.display_name = item.qc_type_id.name + " > " + item.name
            else:
                item.display_name = ""

    @api.onchange('qc_type_id')
    def onchange_qc_type_id(self):
        self.apply = self.qc_type_id.apply

    @api.constrains('name', 'apply', 'qc_type_id')
    def constrain_name_apply(self):
        record = self.env['mes.qc_item'].search(
            [('name', '=', self.name), ('apply', '=', self.apply), ('qc_type_id', '=', self.qc_type_id.id)])
        if len(record) > 1:
            raise ValidationError('The type with the same Name, QC Type and Apply has already existed')

    user_created_id = fields.Many2one('res.partner', string='User Created')
    create_date = fields.Date('Create Date')
    user_updated_id = fields.Many2one('res.partner', string='User Updated')
    update_date = fields.Date('Update Date')
    qc_form_question_id = fields.Many2one('mes.qc_form_questions', string='MES QC Form')


class MESQCStandard(models.Model):
    _name = "mes.qc_standard"
    _description = "MES QC Standard"

    name = fields.Char(string='Name')
    apply = fields.Selection([('iqc', 'IQC'), ('pqc', 'PQC'), ('oqc', 'OQC'), ('mold', 'MOLD'), ('app', 'APP')],
                             string="Apply")
    user_created_id = fields.Many2one('res.partner', string='User Created')
    create_date = fields.Date('Create Date')
    user_updated_id = fields.Many2one('res.partner', string='User Updated')
    update_date = fields.Date('Update Date')
    qc_form_question_id = fields.Many2one('mes.qc_form_questions', string='MES QC Form')
    qc_type_id = fields.Many2one('mes.qc_type', string="QC Type")
    qc_item_id = fields.Many2one('mes.qc_item', string="QC Item")
    display_name = fields.Char(string='Display Name', compute='compute_display_name')

    def compute_display_name(self):
        for item in self:
            print(item.qc_item_id)
            print(item.qc_type_id)
            if (item.qc_item_id.name != False) and (item.qc_type_id.name != False):
                item.display_name = item.qc_type_id.name + " > " + item.qc_item_id.name + " > " + item.name
            else:
                item.display_name = ""

    @api.onchange('qc_type_id')
    def onchange_qc_type_id(self):
        self.apply = self.qc_type_id.apply

    @api.constrains('name', 'apply', 'qc_type_id')
    def constrain_name_apply(self):
        record = self.env['mes.qc_standard'].search(
            [('name', '=', self.name), ('apply', '=', self.apply), ('qc_type_id', '=', self.qc_type_id.id)])
        if record:
            raise ValidationError('The type with the same Name, QC Type and Apply has already existed')


class MESQCTool(models.Model):
    _name = "mes.qc_tool"
    _description = "MES QC Tool"

    name = fields.Char(string='Name')
    apply = fields.Selection([('iqc', 'IQC'), ('pqc', 'PQC'), ('oqc', 'OQC'), ('mold', 'MOLD'), ('app', 'APP')],
                             string="Apply")
    user_created_id = fields.Many2one('res.partner', string='User Created')
    create_date = fields.Date('Create Date')
    user_updated_id = fields.Many2one('res.partner', string='User Updated')
    update_date = fields.Date('Update Date')
    qc_form_question_id = fields.Many2one('mes.qc_form_questions', string='MES QC Form')

    @api.constrains('name', 'apply')
    def constrain_name_apply(self):
        record = self.env['mes.qc_type'].search([('name', '=', self.name), ('apply', '=', self.apply)])
        if len(record) > 1:
            raise ValidationError('The type with the same Name and Apply has already existed')


class MESQCFrequency(models.Model):
    _name = "mes.qc_frequency"
    _description = "MES QC Frequency"

    name = fields.Char(string='Name')
    apply = fields.Selection([('iqc', 'IQC'), ('pqc', 'PQC'), ('oqc', 'OQC'), ('mold', 'MOLD'), ('app', 'APP')],
                             string="Apply")
    user_created_id = fields.Many2one('res.partner', string='User Created')
    create_date = fields.Date('Create Date')
    user_updated_id = fields.Many2one('res.partner', string='User Updated')
    update_date = fields.Date('Update Date')
    qc_form_question_id = fields.Many2one('mes.qc_form_questions', string='MES QC Form')

    @api.constrains('name', 'apply')
    def constrain_name_apply(self):
        record = self.env['mes.qc_type'].search([('name', '=', self.name), ('apply', '=', self.apply)])
        if record:
            raise ValidationError('The type with the same Name and Apply has already existed')
