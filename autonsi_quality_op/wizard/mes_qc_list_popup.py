from odoo import models, fields, api


class MESQualityCheckPopup(models.TransientModel):
    _name = 'mes.qualitychecklist'
    _description = 'List of quality check'

    qc_check_information = fields.Char('QC Check Information')
    mo_id = fields.Many2one('mrp.production', 'MO ID')
    qc_form_id = fields.Many2many('mes.qc_form', 'QC Form ID', compute='compute_qc_form_id')
    state = fields.Selection([('single', 'SingleForm'), ('multipleform', 'MultiForm')], 'Status')
    chosen_state = fields.Boolean(string='Chosen', default=False)

    def action_submit(self, **kwargs):
        print(self)
        print(kwargs)
        for question in self.question_ids:
            print(question)

    def compute_question_ids(self):
        questions = []

        for question in self.env.context['question_id']:
            question_id = self.env['mes.qc_form_questions'].sudo().search([('id', '=', question)])
            questions.append(question_id.id)
        self.question_ids = questions

    def compute_qc_form_id(self):
        print(self.env.context)

    def default_get(self, fields_list):
        result = super(MESQualityCheckPopup, self).default_get(fields_list)
        form_id = self.env['mes.qc_form'].sudo().search([('id', '=', self.env.context['form_id'])])
        result['qc_form_id'] = form_id

        return result

