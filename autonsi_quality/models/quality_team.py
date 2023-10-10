# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import ast
from odoo import models, fields, api

class ShQcTeamType(models.Model):
    _name = 'sh.qc.team.type'
    _description = 'Sh Qc Team Type'
    
    name = fields.Char("Name")
    team_id= fields.Many2one('sh.qc.team')
    check_count = fields.Integer("Check Count", compute='get_check_count')
    alert_count = fields.Integer("Alert Count", compute='get_alert_count')
    pending_qc_count = fields.Integer(
        "Pending QC Count", compute='get_pending_qc_count')
    failed_qc_count = fields.Integer(
        "Failed QC Count", compute='get_failed_qc_count')
    passed_qc_count = fields.Integer(
        "Pass QC Count", compute='get_passed_qc_count')

    
    

    def team_quality_check_action(self):

        if self.name == 'MRP'  or self.name =='Manufacturing':
            return {
                'name': 'Quality Checks',
                        'type': 'ir.actions.act_window',
                        'view_type': 'form',
                        'view_mode': 'tree,form',
                        'domain': [('control_point_id.team', '=', self.team_id.id),('sh_mrp','!=',False)],
                        'res_model': 'sh.mrp.quality.check',
                        'context': {'search_default_control_point': 1, },
                        'target': 'current',
            }
        elif self.name == 'Work-Order':
            view_id = self.env.ref('sh_mrp_qc.wo_quality_check_tree_view')
            return {
                'name': 'Quality Checks',
                        'type': 'ir.actions.act_window',
                        'view_type': 'form',
                        'view_mode': 'tree,form',
                        'domain': [('control_point_id.team', '=', self.team_id.id),('sh_workorder_id','!=',False)],
                        'res_model': 'sh.mrp.quality.check',
                        'context': {'search_default_control_point': 1, },
                        'target': 'current',
                        'views': [(view_id.id, 'tree'),(False,'form')],
            }

    def pending_qc_action(self):

        if self.name == 'MRP'  or self.name =='Manufacturing':
            return {
                'name': 'Pending Quality Checks',
                        'type': 'ir.actions.act_window',
                        'view_type': 'form',
                        'view_mode': 'tree,form',
                        'domain': [('pending_qc', '=', True),('sh_mrp_quality_point_id.team.id', '=', self.team_id.id)],
                        'res_model': 'mrp.production',
                        'target': 'current',
            }
        elif self.name == 'Work-Order':
            return {
                'name': 'Pending Quality Checks',
                        'type': 'ir.actions.act_window',
                        'view_type': 'form',
                        'view_mode': 'tree,kanban,form',
                        'domain': [('pending_qc', '=', True),('sh_workorder_quality_point_id.team.id', '=', self.team_id.id)],
                        'res_model': 'mrp.workorder',
                        'target': 'current',
            }
            
    def failed_qc_action(self):

        if self.name == 'MRP'  or self.name =='Manufacturing':
            return {
                'name': 'Failed Quality Checks',
                        'type': 'ir.actions.act_window',
                        'view_type': 'form',
                        'view_mode': 'tree,form',
                        'domain': [('qc_fail', '=', True), ('sh_mrp_quality_point_id.team.id', '=', self.team_id.id)],
                        'res_model': 'mrp.production',
                        'target': 'current',
            }
        elif self.name == 'Work-Order':
            return {
                'name': 'Failed Quality Checks',
                        'type': 'ir.actions.act_window',
                        'view_type': 'form',
                        'view_mode': 'tree,kanban,form',
                        'domain': [('qc_fail', '=', True), ('sh_workorder_quality_point_id.team.id', '=', self.team_id.id)],
                        'res_model': 'mrp.workorder',
                        'target': 'current',
            }

    def passed_qc_action(self):

        if self.name == 'MRP'  or self.name =='Manufacturing':
            return {
                'name': 'Passed Quality Checks',
                        'type': 'ir.actions.act_window',
                        'view_type': 'form',
                        'view_mode': 'tree,form',
                        'domain': [('qc_pass', '=', True), ('sh_mrp_quality_point_id.team.id', '=', self.team_id.id)],
                        'res_model': 'mrp.production',
                        'target': 'current',
            }
        elif self.name == 'Work-Order':
            return {
                'name': 'Passed Quality Checks',
                        'type': 'ir.actions.act_window',
                        'view_type': 'form',
                        'view_mode': 'tree,kanban,form',
                        'domain': [('qc_pass', '=', True), ('sh_workorder_quality_point_id.team.id', '=', self.team_id.id)],
                        'res_model': 'mrp.workorder',
                        'target': 'current',
            }

    def partially_passed_qc_action(self):
        return {
            'name': 'Partially Passed Quality Checks',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'domain': [('qc_pass', '=', True), ('move_ids_without_package.sh_quality_point_id.team.id', '=', self.team_id.id)],
                    'res_model': 'stock.picking',
                    'context': {'search_default_picking_type': 1, },
                    'target': 'current',
        }

    def get_pending_qc_count(self):
        for rec in self:
            
            if rec.name == 'MRP' or rec.name == 'Manufacturing':
                rec.pending_qc_count = self.env['mrp.production'].search_count(
                    [('pending_qc', '=', True), ('sh_mrp_quality_point_id.team.id', '=', rec.team_id.id)])
            elif rec.name == 'Work-Order':
                rec.pending_qc_count = self.env['mrp.workorder'].search_count(
                    [('pending_qc', '=', True), ('sh_workorder_quality_point_id.team.id', '=', rec.team_id.id)])
            
    def get_failed_qc_count(self):
        for rec in self:
            
            if rec.name == 'MRP'  or self.name =='Manufacturing':
                rec.failed_qc_count = self.env['mrp.production'].search_count(
                    [('qc_fail', '=', True), ('sh_mrp_quality_point_id.team.id', '=', rec.team_id.id)])
            elif rec.name == 'Work-Order':
                rec.failed_qc_count = self.env['mrp.workorder'].search_count(
                    [('qc_fail', '=', True), ('sh_workorder_quality_point_id.team.id', '=', rec.team_id.id)])

    def get_passed_qc_count(self):
        for rec in self:
            
            if rec.name == 'MRP'  or rec.name =='Manufacturing':
                rec.passed_qc_count = self.env['mrp.production'].search_count(
                    [('qc_pass', '=', True), ('sh_mrp_quality_point_id.team.id', '=', rec.team_id.id)])
            elif rec.name == 'Work-Order':
                rec.passed_qc_count = self.env['mrp.workorder'].search_count(
                    [('qc_pass', '=', True), ('sh_workorder_quality_point_id.team.id', '=', rec.team_id.id)])

    

                 
    def get_check_count(self):
        for rec in self:
            if rec.name == 'MRP'  or rec.name =='Manufacturing':
                rec.check_count = self.env['sh.mrp.quality.check'].search_count(
                    [('control_point_id.team.id', '=', rec.team_id.id),('sh_mrp','!=',False)])
            elif rec.name == 'Work-Order':
                rec.check_count = self.env['sh.mrp.quality.check'].search_count(
                    [('control_point_id.team.id', '=', rec.team_id.id),('sh_workorder_id','!=',False)])

class ShQcTeam(models.Model):
    _inherit = ['mail.alias.mixin', 'mail.thread', 'mail.activity.mixin']
    _name = 'sh.qc.team'
    _description = "Quality Team"

    sh_logged_user = fields.Many2one(
        'res.users', 'User', readonly=True, default=lambda self: self.env.user)
    name = fields.email = fields.Char('Title', required=True)
    email = fields.Char('Email')
    user_ids = fields.Many2many("res.users", string="Users")
    sh_employee = fields.Many2one('hr.employee', string="Employee")
    company_id = fields.Many2one(
        'res.company', string="Company", default=lambda self: self.env.company, required=True)
    name_id = fields.Char('Id#', readonly=True, copy=False)
    
    alias_id = fields.Many2one(
        'mail.alias', 'Alias', ondelete="restrict")

    def _alias_get_creation_values(self):
        values = super(ShQcTeam, self)._alias_get_creation_values()
        values['alias_model_id'] = self.env['ir.model']._get('sh.qc.team').id
        if self.id:
            values['alias_defaults'] = defaults = ast.literal_eval(self.alias_defaults or "{}")
        return values
    
    @api.model
    def create(self, vals):
        if 'company_id' in vals:
            vals['name_id'] = self.env['ir.sequence'].with_context(
                with_company=vals['company_id']).next_by_code('quality.team')
        res = super(ShQcTeam, self).create(vals)
        self.env['sh.qc.team.type'].sudo().create({'name':'Manufacturing','team_id':res.id})
        
        return res
