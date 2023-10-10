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


class MasterManufacturingOrder(models.Model):
    _inherit = "mrp.masterproduction"
    quality_check_ids = fields.One2many('sh.mrp.quality.check', 'mmo_id', string='Quality Checks')

    @api.onchange('mmo_product_tmpl_id')
    def _onchange_product_id_mmo(self, work_center_id=None):
        super()._onchange_product_id_mmo()
        print("On change quality")
        self.quality_check_ids = [(5, 0, 0)]
        for mo_line in self.mo_line_ids:
            if mo_line.check_pqc:
                mo_line.need_qc = True
                quality_point_id = self.env['sh.qc.point'].sudo().search([
                    ('product_id', '=', mo_line.product_id.id),
                    ('operation', '=', mo_line.picking_type_id.id),
                    '|', ('team.user_ids.id', 'in', [self.env.uid]), ('team', '=', False)], limit=1,
                    order='create_date desc')
                mo_line.sh_mrp_quality_point_id = quality_point_id.id

                mes_qc_form_id = self.env['mes.qc_form'].sudo().search([('product_id', '=', mo_line.product_id.id)])
                if len(mes_qc_form_id) > 1:
                    mo_line.mes_qc_form_id = mes_qc_form_id[0]
                else:
                    if mes_qc_form_id:
                        mo_line.mes_qc_form_id = mes_qc_form_id
                    else:
                        new_qc_form_data = {
                            'name': mo_line.product_id.name,
                            'product_id': mo_line.product_id.id
                        }
                        new_qc_form = self.env['mes.qc_form'].sudo().create(new_qc_form_data)
                        mo_line.mes_qc_form_id = new_qc_form
                control_point_id = self.env['sh.qc.point'].sudo().search([('product_id', '=', mo_line.product_id.id)])
                new_mrp_qc_data = {
                    'product_id': mo_line.product_id.id,
                    'sh_date': self.date_planned_start,
                    'control_point_id': control_point_id.id,
                    'sh_control_point': control_point_id.product_id.name,
                    'qc_type': control_point_id.type,
                    'state': 'draft'

                }
                new_mrp_qc = self.env['sh.mrp.quality.check'].sudo().create(new_mrp_qc_data)
                mo_line.sh_mrp_quality_check_ids = new_mrp_qc
                print(new_mrp_qc)
                self.quality_check_ids = [(4, new_mrp_qc.id)]
