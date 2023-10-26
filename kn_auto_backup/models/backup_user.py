from odoo import models, fields

class backup_user(models.Model):
    _name = 'kn.auto.backup_user'
    _description = 'kn_auto_backup.kn_auto_backup_user'
   
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        help='Select a partner',
    )