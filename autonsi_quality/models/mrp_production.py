# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api
from odoo.exceptions import ValidationError

import json
import datetime
import math
import re

from collections import defaultdict
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_round, float_is_zero, format_datetime
from odoo.tools.misc import format_date

from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES

import logging

_logger = logging.getLogger(__name__)


class View(models.Model):
    _inherit = 'ir.ui.view'
    type = fields.Selection(
        selection_add=[('qualitycheckview', "Quality Check View")]
    )


class ActWindowView(models.Model):
    _inherit = 'ir.actions.act_window.view'
    view_mode = fields.Selection(
        selection_add=[('qualitycheckview', "Quality Check View")],
        ondelete={'qualitycheckview': 'cascade'}
    )


class Manufacturing(models.Model):
    _inherit = 'mrp.production'

    sh_mrp_quality_check_ids = fields.One2many(
        'sh.mrp.quality.check', 'sh_mrp', string="Mrp Quality Checks ")

    # sh_mrp_quality_check_ids_nbr = fields.Integer(
    #     compute='_compute_sh_mrp_quality_check_ids_nbr', string='# of Sales Orders')

    sh_mrp_pass_fail_ids = fields.One2many(
        'sh.mrp.pass.fail', 'mrp_id', string="Mrp Pass Fail Quality Checks")
    sh_mrp_pics_ids = fields.One2many(
        'sh.mrp.pics', 'mrp_id', string="Mrp pics Quality Checks")
    sh_mrp_measurement_ids = fields.One2many(
        'sh.mrp.measurement', 'mrp_id', string="Mrp measurement Quality Checks")
    sh_mrp_qc_measurement_ids = fields.One2many(
        'sh.mrp.qc.measurement', 'mrp_id', string="Mrp QC measurement Quality Checks")
    need_qc = fields.Boolean(
        "Need QC")
    pending_qc = fields.Boolean(
        "Pending QC", compute='_compute_check_qc', search='search_mrp_pending_qc')

    qc_fail = fields.Boolean(
        "QC Fail", compute='_compute_check_qc', search='search_mrp_fail_qc')
    qc_pass = fields.Boolean(
        "QC Pass", compute='_compute_check_qc', search='search_mrp_pass_qc')

    is_mandatory = fields.Boolean(
        "QC Mandatory", compute='_compute_check_qc_mandatory')

    attachment_ids = fields.Many2many(
        'ir.attachment', string="QC Pictures", copy=False)

    sh_mrp_quality_point_id = fields.Many2one(
        'sh.qc.point', 'Quality Control Point')

    partner_id = fields.Many2one('res.partner', 'Contact')

    qc_count = fields.Integer('Quality Checks', compute='_compute_get_qc_count')


    def search_mrp_pending_qc(self, operator, value):
        rec_ids = []
        for rec_id in self.search([]):
            if rec_id.pending_qc:
                rec_ids.append(rec_id.id)
        return [('id', 'in', rec_ids)]

    def search_mrp_fail_qc(self, operator, value):
        rec_ids = []
        for rec_id in self.search([]):
            if rec_id.qc_fail:
                rec_ids.append(rec_id.id)
        return [('id', 'in', rec_ids)]

    def search_mrp_pass_qc(self, operator, value):
        rec_ids = []
        for rec_id in self.search([]):
            if rec_id.qc_pass:
                rec_ids.append(rec_id.id)
        return [('id', 'in', rec_ids)]

    def _compute_check_qc_mandatory(self):
        if self:
            for rec in self:
                rec.is_mandatory = False
                if rec.sh_mrp_quality_point_id and rec.sh_mrp_quality_point_id.is_mandatory:
                    rec.is_mandatory = True

    def _compute_check_qc(self):
        if self:
            for rec in self:
                rec.qc_pass = False
                rec.qc_fail = False
                rec.pending_qc = False
                if rec.need_qc == True:
                    rec.pending_qc = True

                last_quality_check = self.env['sh.mrp.quality.check'].search(
                    [('product_id', '=', rec.product_id.id), ('sh_mrp', '=', rec.id)], limit=1,
                    order='create_date desc')
                if last_quality_check:
                    for qc in last_quality_check:

                        if qc.state == 'fail':
                            rec.qc_fail = True
                            rec.qc_pass = False
                            rec.pending_qc = False

                        if qc.state == 'pass':
                            rec.qc_pass = True
                            rec.qc_fail = False
                            rec.pending_qc = False

    def quality_point(self):
        if self.product_id:
            quality_point_id = self.env['sh.qc.point'].sudo().search([
                ('product_id', '=', self.product_id.id),
                ('operation', '=', self.picking_type_id.id),
                '|', ('team.user_ids.id', 'in', [self.env.uid]), ('team', '=', False)], limit=1,
                order='create_date desc')

        if quality_point_id:
            self.sh_mrp_quality_point_id = quality_point_id.id

        # if len(self.sh_mrp_quality_check_ids) >= self.sh_mrp_quality_point_id.number_of_test and self.sh_mrp_quality_point_id.number_of_test != 0:
        #
        #     message = 'You Maximum number of allowed Test is Over Now'
        #
        #     return {
        #         'name': 'NO. of Allowed Quality Checks',
        #         'type': 'ir.actions.act_window',
        #         'view_type': 'form',
        #         'view_mode': 'form',
        #         'res_model': 'sh.mrp.allow.qc.measurement',
        #         'context': {'default_mrp_id': self.id, 'default_sh_quality_point_id': self.sh_mrp_quality_point_id.id, 'default_sh_message': message, 'default_product_id': self.product_id.id},
        #         'target': 'new',
        #     }

            # return {
            #     'type': 'ir.actions.act_url',
            #     'name': "Test Survey",
            #     'target': '_blank',
            #     'url': '/qc_1/%s/%s/%s' % (
            #     self.sh_mrp_quality_check_ids.mes_qc_form_id.id, self.sh_mrp_quality_check_ids.id, self.id),
            # }
        sname = 'Quality Checks Popup'
        viewid = 'autonsi_quality.sh_mr_quality_check_wizard_form_view'
        viewidname = self.env.ref(viewid).id

        _logger.warning('--viewidname %s', viewidname)
        print(self.env.context)
        question_context = []
        defaultquestion_ids = []
        for question in self.sh_mrp_quality_check_ids.mes_qc_form_id.question_ids:
            defaultquestion_ids.append(question)
        context_data = {
            'quality_check_id': self.sh_mrp_quality_check_ids.id,
            'form_id': self.sh_mrp_quality_check_ids.mes_qc_form_id.id,
            'question_id': question_context,
            'default_question_ids': defaultquestion_ids,
            'view_mode': "MO Quality Check"
        }
        for type in self.sh_mrp_quality_check_ids.mes_qc_form_id.qc_sop_type:
            question = self.sh_mrp_quality_check_ids.mes_qc_form_id
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


    def action_quality_alert(self):
        line_ids = []
        if self:
            vals = {
                'product_id': self.product_id.id,
                'partner_id': self.partner_id.id,
            }
            line_ids.append((0, 0, vals))
        return {
            'name': 'Quality Alert',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.mrp.qc.alert',
            'context': {'default_alert_ids': line_ids},
            'target': 'new',
        }

    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super(Manufacturing, self)._onchange_product_id()

        if self.product_id:
            quality_point_id = self.env['sh.qc.point'].sudo().search([
                ('product_id', '=', self.product_id.id),
                ('operation', '=', self.picking_type_id.id),
                '|', ('team.user_ids.id', 'in', [self.env.uid]), ('team', '=', False)], limit=1,
                order='create_date desc')

            if quality_point_id:
                self.need_qc = True
                self.sh_mrp_quality_point_id = quality_point_id.id

            else:
                self.need_qc = False

        return res



    def _compute_get_qc_count(self):
        if self:
            for rec in self:
                rec.qc_count = 0
                qc = self.env['sh.mrp.quality.check'].search(
                    [('sh_mrp', '=', rec.id)])
                rec.qc_count = len(qc.ids)

    def open_quality_check(self):
        po = self.env['sh.mrp.quality.check'].search(
            [('sh_mrp', '=', self.id)])
        action = self.env.ref(
            'autonsi_quality.mrp_quality_check_action').read()[0]
        action['context'] = {
            'domain': [('id', 'in', po.ids)]

        }
        action['domain'] = [('id', 'in', po.ids)]
        return action

    def button_mark_done(self):
        all_quality_check_is_done = True
        for quality_check in self.sh_mrp_quality_check_ids:
            if quality_check.state == 'draft':
                all_quality_check_is_done = False
        if all_quality_check_is_done:
            return super(Manufacturing, self).button_mark_done()
        else:
            print('Mark UnDone')
            raise ValidationError("All quality checks needs to be done")

    def _pre_button_mark_done(self):
        productions_to_immediate = self._check_immediate()
        if productions_to_immediate:
            return productions_to_immediate._action_generate_immediate_wizard()

        for production in self:
            if float_is_zero(production.qty_producing, precision_rounding=production.product_uom_id.rounding):
                _logger.info('-----The quantity to produce must be positiv')
                raise UserError(_('The quantity to produce must be positive!'))
            if production.move_raw_ids and not any(production.move_raw_ids.mapped('quantity_done')):
                raise UserError(_("You must indicate a non-zero amount consumed for at least one of your components"))

        consumption_issues = self._get_consumption_issues()
        if consumption_issues:
            _logger.info('-----The quantity to produce must be positiv 1111')
            return self._action_generate_consumption_wizard(consumption_issues)

        quantity_issues = self._get_quantity_produced_issues()
        if quantity_issues:
            _logger.info('-----The quantity to produce must be positiv 2222')
            return self._action_generate_backorder_wizard(quantity_issues)
        return True



