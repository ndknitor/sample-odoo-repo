# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import logging
from collections import defaultdict, namedtuple
import datetime
from dateutil.relativedelta import relativedelta

from odoo import SUPERUSER_ID, _, api, fields, models, registry
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools import float_compare, float_is_zero, html_escape
from odoo.tools.misc import split_every

from odoo.tools.misc import OrderedSet, format_date, groupby as tools_groupby
from odoo.tools import float_compare, float_round, float_is_zero, format_datetime
from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES

_logger = logging.getLogger(__name__)

semiproductlist = {}


class ProductTemplate(models.Model):
    _inherit = "product.template"

    fg_product_is = fields.Boolean(string="Is FG Product", help="This is FG Product")


class ManufacturingOrder(models.Model):
    _inherit = "mrp.production"
    mmo_id = fields.Many2one("mrp.masterproduction", "Master Manufacturing Order")
    mo_name = fields.Many2one("mrp.production", string='Reference')
    level = fields.Integer(string='Operation level', default=1)
    check_pqc = fields.Boolean(string='Check PQC', default=True)
    pqc_result = fields.Selection([
        ('pass', 'PASS'),
        ('not pass', 'NOT PASS')], string='PRC Result')
    workcenter_id = fields.Many2one("mrp.workcenter", string='Work Center')
    need_qc = fields.Boolean(
        "Need QC")
    operation_name = fields.Char('Operation Name')
    def change_bom_id(self):
        if not self.product_id and self.bom_id:
            self.product_id = self.bom_id.product_id or self.bom_id.product_tmpl_id.product_variant_ids[:1]
        self.product_qty = self.mmo_id.quantity
        self.product_uom_id = self.bom_id and self.bom_id.product_uom_id.id or self.product_id.uom_id.id
        self.move_raw_ids = [(2, move.id) for move in self.move_raw_ids.filtered(lambda m: m.bom_line_id)]
        self.move_finished_ids = [(2, move.id) for move in self.move_finished_ids]
        picking_type_id = self._context.get('default_picking_type_id')
        picking_type = picking_type_id and self.env['stock.picking.type'].browse(picking_type_id)
        self.picking_type_id = picking_type or self.bom_id.picking_type_id or self.picking_type_id

class WorkOrder(models.Model):
    _inherit = "mrp.workorder"
    mmo_id = fields.Many2one("mrp.masterproduction", "Master Manufacturing Order")


class StockMove(models.Model):
    _inherit = "stock.move"
    name = fields.Char(string="Description", default='Product move', required=True)


class MasterManufacturingOrder(models.Model):
    _name = "mrp.masterproduction"
    _description = "Master Manufacturing Order"
    name = fields.Char(string='Name')
    mmo_id = fields.Many2one('product.template', 'Product', domain=[('fg_product_is', '=', True)])
    quantity = fields.Integer(string='Quantity', required=True, default=1)
    sale_order_id = fields.Many2one('sale.order', 'Sale Order')

    @api.model
    def _get_default_date_planned_start(self):
        if self.env.context.get('default_date_deadline'):
            return fields.Datetime.to_datetime(self.env.context.get('default_date_deadline'))
        return datetime.datetime.now()

    product_id = fields.Many2one(
        'product.product', 'Product',
        domain=[('fg_product_is', '=', True)], check_company=True,
        states={'draft': [('readonly', False)]})
    mmo_bom_id = fields.Many2one(
        'mrp.bom', 'Bill of Material', states={'draft': [('readonly', False)]},
        domain="""[
        '&',
            '|',
                ('company_id', '=', False),
                ('company_id', '=', company_id),
            '&',
                '|',
                    ('product_id','=',product_id),
                    '&',
                        ('product_tmpl_id.product_variant_ids','=',product_id),
                        ('product_id','=',False),
        ('type', '=', 'normal')]""",
        check_company=True,
        help="Bill of Materials allow you to define the list of required components to make a finished product.")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('progress', 'In Progress'),
        ('to_close', 'To Close'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], string='State', copy=False, index=True, readonly=True,
        store=True, tracking=True,
        help=" * Draft: The MO is not confirmed yet.\n"
             " * Confirmed: The MO is confirmed, the stock rules and the reordering of the components are trigerred.\n"
             " * In Progress: The production has started (on the MO or on the WO).\n"
             " * To Close: The production is done, the MO has to be closed.\n"
             " * Done: The MO is closed, the stock moves are posted. \n"
             " * Cancelled: The MO has been cancelled, can't be confirmed anymore.", default='draft')
    mmo_product_tmpl_id = fields.Many2one('product.template', 'Product Template', related='product_id.product_tmpl_id')
    date_planned_start = fields.Datetime(
        'Scheduled Date', copy=False, default=_get_default_date_planned_start,
        help="Date at which you plan to start the production.",
        index=True, required=True)

    company_id = fields.Many2one(
        'res.company', 'Company', default=lambda self: self.env.company,
        index=True, required=True)

    mo_line_ids = fields.One2many('mrp.production', 'mmo_id', string='Manufacturing Orders')
    wo_line_ids = fields.One2many('mrp.workorder', 'mmo_id', string='Work Orders')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('mrp.masterproduction')
        return super(MasterManufacturingOrder, self).create(vals)

    @api.onchange('mmo_product_tmpl_id')
    def _onchange_product_id_mmo(self, work_center_id=None):
        self.mo_line_ids = [(5, 0, 0)]
        if self.product_id.bom_ids and self.product_id:
            self.mmo_bom_id = self.env['mrp.bom'].search([('id', '=', self.product_id.bom_ids.id)])
        lines_created = []

        semiproductlist.clear()
        if self.product_id:
            semiproductlist[self.product_id] = 0
        self.calculate_semi_bom()
        operation_type = self.env['stock.picking.type'].search([])
        operationtypeid = 0
        defaultsrcid = 0
        defaultdestid = 0
        for operationtype in operation_type:
            if operationtype.name == "Manufacturing":
                operationtypeid = operationtype.id
                defaultsrcid = operationtype.default_location_src_id.id
                defaultdestid = operationtype.default_location_dest_id.id
        product_list_length = len(semiproductlist)
        for line in semiproductlist:
            bom = self.env['mrp.bom'].search([('product_tmpl_id', '=', line.id)])
            operation = self.env['mrp.routing.workcenter'].search([('bom_id', '=', bom.id)])
            if work_center_id != None:
                operation_center = work_center_id
            else:
                operation_center = operation.workcenter_id.id
            if semiproductlist[line] != 0:
                lines_created.append((0, 0, {'product_id': line.id,
                                             'company_id': self.company_id.id,
                                             'date_planned_start': self.date_planned_start,
                                             'picking_type_id': operationtypeid,
                                             'location_src_id': defaultsrcid,
                                             'workcenter_id': operation_center,
                                             'location_dest_id': defaultsrcid,
                                             'product_uom_id': 1,
                                             'consumption': 'flexible',
                                             'level': product_list_length - 1,
                                             'product_qty': self.quantity,
                                             # 'qty_producing' : self.quantity,
                                             'bom_id': bom.id}))
            elif semiproductlist[line] == 0:
                lines_created.append((0, 0, {'product_id': line.id,
                                             'company_id': self.company_id.id,
                                             'date_planned_start': self.date_planned_start,
                                             'picking_type_id': operationtypeid,
                                             'location_src_id': defaultsrcid,
                                             'workcenter_id': operation_center,
                                             'location_dest_id': defaultdestid,
                                             'product_uom_id': 1,
                                             'consumption': 'flexible',
                                             'level': product_list_length - 1,
                                             'product_qty': self.quantity,
                                             # 'qty_producing': self.quantity,
                                             'bom_id': bom.id}))
            product_list_length -= 1
        self.mo_line_ids = lines_created[::-1]

        for mo_line in self.mo_line_ids:
            mo_line._onchange_product_id()
            mo_line.change_bom_id()
            mo_line._onchange_move_raw()
            mo_line._onchange_product_qty()
            # mo_line._action_confirm()
            # component_lines_created = []
            # for bom in mo_line.bom_id:
            #     for bom_line in bom.bom_line_ids:
            #         virtuallocation = self.env['stock.location'].search(
            #             [('complete_name', '=', 'Virtual Locations/Production')])
            #         preproduction = self.env['stock.location'].search([('complete_name', '=', 'WH/Pre-Production')])
            #         vals = {'name': 'WH/Stock/Material -> WH/Pre-production',
            #                 'reference': 'WH/Stock/Material -> WH/Pre-production',
            #                 'company_id': self.company_id.id,
            #                 'date': self.date_planned_start,
            #                 'location_id': preproduction.id,
            #                 'location_dest_id': virtuallocation.id,
            #                 'product_id': bom_line.product_id.id,
            #                 'product_uom': mo_line.product_uom_id.id,
            #                 'product_uom_qty': mo_line.product_qty,
            #                 'procure_method': 'make_to_order',
            #                 'warehouse_id': 1
            #                 }
            #         move = self.env['stock.move'].create(vals)
            #         component_lines_created.append(move.id)
            # component_lines_created.reverse()
            # mo_line.write({'move_finished_ids': component_lines_created})
            print(mo_line)
    def calculate_semi_bom(self, product_id=None, level=1):
        hassemi = False
        if product_id != None:
            for line in product_id.bom_ids.bom_line_ids:
                if line.product_id.semi_product_is:
                    hassemi = True
                    semiproductlist[line.product_id] = level
                    return self.calculate_semi_bom(line.product_id, level + 1)
            if hassemi == False:
                return

        if product_id == None:
            for line in self.mmo_bom_id.bom_line_ids:
                if line.product_id.semi_product_is:
                    hassemi = True
                    semiproductlist[line.product_id] = level
                    self.calculate_semi_bom(line.product_id, 2)
            if hassemi == False:
                return

    def action_confirm(self):
        self.state = 'confirmed'
        wo_lines_created = []
        work_order_ids = []
        for mo_line in self.mo_line_ids:
            wo_line = self.create_workorder(mo_line)
            print(wo_line)
            wo_lines_created.append(wo_line)
            mo_line.mo_name = mo_line
            mo_line.operation_name = wo_line[0]['name']
        for wo_lines in wo_lines_created:
            work_order = self.env['mrp.workorder'].create(wo_lines)
            work_order_ids.append(work_order.id)
        # for mo_line in self.mo_line_ids:
        #     work_order_mo = self.env['mrp.workorder'].search([('production_id', '=', mo_line.id)])
        #     mo_line.workorder_ids = work_order_mo
        # self.add_bom_line()

    def create_workorder(self, mo_line):
        wo_ids = []
        for production in mo_line:
            if not production.bom_id or not production.product_id:
                continue

            product_qty = mo_line.product_qty
            exploded_boms, dummy = production.bom_id.explode(production.product_id,
                                                             product_qty / production.bom_id.product_qty,
                                                             picking_type=production.bom_id.picking_type_id)

            for bom, bom_data in exploded_boms:
                # If the operations of the parent BoM and phantom BoM are the same, don't recreate work orders.
                if not (bom.operation_ids and (not bom_data['parent_line'] or bom_data[
                    'parent_line'].bom_id.operation_ids != bom.operation_ids)):
                    continue
                for operation in bom.operation_ids:
                    if operation._skip_operation_line(bom_data['product']):
                        continue
                    wo_ids += [{
                        'name': operation.name,
                        'production_id': production.id,
                        'workcenter_id': operation.workcenter_id.id,
                        'product_uom_id': production.product_uom_id.id,
                        'operation_id': operation.id,
                        'state': 'pending',
                        'duration_expected': 60
                    }]

        return wo_ids

    def add_bom_line(self):
        for mo_line in self.mo_line_ids:
            component_lines_created = []
            for bom in mo_line.bom_id:
                for bom_line in bom.bom_line_ids:
                    virtuallocation = self.env['stock.location'].search(
                        [('complete_name', '=', 'Virtual Locations/Production')])
                    preproduction = self.env['stock.location'].search([('complete_name', '=', 'WH/Pre-Production')])
                    vals = {'name': 'WH/Stock/Material -> WH/Pre-production',
                            'reference': 'WH/Stock/Material -> WH/Pre-production',
                            'company_id': self.company_id.id,
                            'date': self.date_planned_start,
                            'location_id': preproduction.id,
                            'location_dest_id': virtuallocation.id,
                            'product_id': bom_line.product_id.id,
                            'product_uom': mo_line.product_uom_id.id,
                            'product_uom_qty': mo_line.product_qty,
                            'procure_method': 'make_to_order',
                            'warehouse_id': 1
                            }
                    move = self.env['stock.move'].create(vals)
                    component_lines_created.append(move.id)
            mo_line.write({'move_raw_ids': component_lines_created})

    def action_manufacturing_order(self):
        return {'name': 'Manufacturing Order List',
                'view_type': 'list,form',

                'view_mode': 'list,form',

                'res_model': 'mrp.production',
                'domain': [('id', 'in', self.mo_line_ids.ids)],
                'type': 'ir.actions.act_window',
                'target': 'current'}

    def create_mmo(self, product_id, work_center_id, quantity, date, sale_order_id):
        mmo = self.env['mrp.masterproduction'].create({
            'product_id': product_id,
            'date_planned_start': date,
            'quantity': quantity,
            'sale_order_id': sale_order_id,
        })
        mmo._onchange_product_id_mmo(work_center_id)
        return mmo

