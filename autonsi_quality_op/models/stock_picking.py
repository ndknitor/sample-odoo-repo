import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    def create(self, vals):
        program = super(StockMove, self).create(vals)
        if program.picking_id:
            _logger.warning('--include_qc %s', program.picking_id.picking_type_id.include_qc)
            if program.picking_id.picking_type_id.include_qc == True:
                program.picking_id.quality_check_ids = [
                    (0, 0, {'stock_picking_id': program.picking_id.id, 'stock_move_id': program.id})]
        else:
            _logger.warning('--picking id not')
        return program

    def write(self, vals):
        program = super(StockMove, self).write(vals)
        for channel in self:
            if channel.picking_id:
                _logger.warning('--write include_qc %s', channel.picking_id.picking_type_id.include_qc)
                if channel.picking_id.picking_type_id.include_qc == True:
                    check = 0
                    for temp in channel.picking_id.quality_check_ids:
                        if temp.stock_move_id.id == channel.id:
                            check = 1
                    if check == 0:
                        channel.picking_id.quality_check_ids = [
                            (0, 0, {'stock_picking_id': channel.picking_id.id, 'stock_move_id': channel.id})]
        return program


class Picking(models.Model):
    _inherit = 'stock.picking'

    include_qc = fields.Boolean(string="Include QC", compute='_compute_include_qc')
    quality_check_ids = fields.One2many('sh.mrp.quality.check', 'stock_picking_id')

    @api.depends('picking_type_id')
    def _compute_include_qc(self):
        self.include_qc = self.picking_type_id.include_qc

    def preview_qc_form(self):
        # mes_qc_form_id = self.quality_check_ids[0].mes_qc_form_id.id
        # mes_qc_form = self.env['mes.qc_form'].browse([mes_qc_form_id])
        # return mes_qc_form.preview_qc_form()
        mes_qc_form_id = []
        question_list = []

        sname = 'Quality List'
        viewid = 'autonsi_quality_op.sh_mr_quality_list_wizard_form_view'
        viewidname = self.env.ref(viewid).id
        defaultquestion_ids = []
        question_context = []

        for quality_check in self.quality_check_ids:
            mes_qc_form_id.append(quality_check.mes_qc_form_id.id)
        print(mes_qc_form_id)
        mes_qc_form = self.env['mes.qc_form'].sudo().search([('id', 'in', mes_qc_form_id)])
        print(mes_qc_form)
        for form in mes_qc_form:
            for question in form.question_ids:
                defaultquestion_ids.append(question)
        context_data = {
            'form_id': mes_qc_form_id,
            'question_id': question_context,
            'default_question_ids': defaultquestion_ids,
            'view_mode': "inventory quality check"
        }
        question_list_data = []
        for form in mes_qc_form:
            print(form.qc_sop_type)
            append_object = {form.qc_sop_type.name: form.name}
            question_list.append(append_object)
            context_data['form_selection'] = question_list
            # for type in self.sh_mrp_quality_check_ids.mes_qc_form_id.qc_sop_type:
            #     question = self.sh_mrp_quality_check_ids.mes_qc_form_id
            #     append_object = {'qc_sop_type': type.name}
            #     question_context.append(append_object)
            if form.qc_sop_type.name == "Matrix":
                answer_ids = []
                matrix_row_ids = []
                matrix_data = {}
                for answer in form.answers_ids:
                    print(answer.value)
                    answer_ids.append(answer.value)
                for matrix_row in form.matrix_row_ids:
                    matrix_row_ids.append(matrix_row.value)
                matrix_data['answer_ids'] = answer_ids
                matrix_data['matrix_rows_ids'] = matrix_row_ids
                question_list_data.append(matrix_data)
            if form.qc_sop_type.name == 'Raw Material':
                raw_material = {}
                raw_material['mes_qc_type'] = form.mes_qc_type_ids.name
                raw_material['mes_qc_item'] = form.mes_qc_item_ids.name
                raw_material['n_values'] = form.n_values
                raw_material['units'] = form.units.name
                question_list_data.append(raw_material)
            if form.qc_sop_type.name == 'Material':
                material_data = {}
                material_data['mes_qc_type'] = form.mes_qc_type_ids.name
                material_data['mes_qc_item'] = form.mes_qc_item_ids.name
                material_data['mes_qc_standard'] = form.mes_qc_standard_ids.name
                material_data['mes_qc_tool'] = form.mes_qc_tool_ids.name
                material_data['mes_qc_frequency'] = form.mes_qc_frequency_ids.name
                question_list_data.append(material_data)
            if form.qc_sop_type.name == 'After Setting' or form.qc_sop_type.name == 'SEMI LOT':
                after_setting_data = {}
                after_setting_data['mes_qc_type'] = form.mes_qc_type_ids.name
                after_setting_data['mes_qc_item'] = form.mes_qc_item_ids.name
                after_setting_data['mes_qc_standard'] = form.mes_qc_standard_ids.name
                after_setting_data['mes_qc_tool'] = form.mes_qc_tool_ids.name
                after_setting_data['mes_qc_frequency'] = form.mes_qc_frequency_ids.name
                question_list_data.append(after_setting_data)
            if form.qc_sop_type.name == 'After QC':
                oqc_data = {}
                oqc_data['mes_qc_type'] = form.mes_qc_type_ids.name
                oqc_data['mes_qc_item'] = form.mes_qc_item_ids.name
                oqc_data['mes_qc_standard'] = form.mes_qc_standard_ids.name
                oqc_data['mes_qc_tool'] = form.mes_qc_tool_ids.name
                oqc_data['mes_qc_frequency'] = form.mes_qc_frequency_ids.name
                question_list_data.append(oqc_data)
        context_data['data'] = question_list_data
        print(question_list)
        return {
            'name': sname,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mes.qualitychecklist',
            'context': context_data,
            'type': 'ir.actions.act_window',
            'target': 'new'
        }


class PickType(models.Model):
    _inherit = 'stock.picking.type'

    include_qc = fields.Boolean(string="Include QC")


class Picking(models.Model):
    _inherit = 'mes.mfg.process.sub'

    @api.onchange('include_qc')
    def _onchange_include_qc(self):
        if self.include_qc == True:
            stock_picking = self.env['stock.picking.type'].search([
                ('id', '=', self.picking_type_id.id)
            ])
            stock_picking.write({'include_qc': True})
        if self.include_qc == False:
            stock_picking = self.env['stock.picking.type'].search([
                ('id', '=', self.picking_type_id.id)
            ])
            stock_picking.write({'include_qc': False})
