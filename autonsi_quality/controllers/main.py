import json
import logging
import werkzeug

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import fields, http, SUPERUSER_ID, _
from odoo.addons.base.models.ir_ui_view import keep_query
from odoo.exceptions import UserError
from odoo.http import request, content_disposition
from odoo.osv import expression
from odoo.tools import format_datetime, format_date, is_html_empty

_logger = logging.getLogger(__name__)


class QualityChecksWeb(http.Controller):
    @http.route('/qc_1/<string:form_id>/<string:qc_id>/<string:mo_id>',type='http', auth='user', website=True)
    def quality_check_route(self, form_id, qc_id,mo_id, **kwargs):
        print(self)
        print(form_id)
        form = request.env['mes.qc_form'].search([('id','=',form_id)])
        print(form)
        print(form.question_ids)
        return http.request.render('autonsi_quality.test_form', {
            'question_ids': form.question_ids,'qc_id': qc_id, 'mo_id': mo_id
        })

    @http.route('/submit_qc_form', type='http', auth='public',csrf=False, website=True)
    def submit_qc_form(self, **kwargs):
        cr, uid, context = request.cr, request.uid, request.context
        print(cr)
        print(uid)
        print(context)
        print(kwargs)
        quality_check_ids = request.env['sh.mrp.quality.check'].search([('id','=',kwargs['quality_check_id'])])
        mo_id = request.env['mrp.production'].search([('id','=',kwargs['manufacturing_order_id'])])
        print(quality_check_ids)
        print(mo_id)
        if 'Pass or Fail' in kwargs:
            quality_check_ids.state = 'pass'
        else:
            quality_check_ids.state = 'fail'

        return http.request.render('autonsi_quality.test_form_thank_you')
