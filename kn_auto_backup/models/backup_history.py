from odoo import models, fields

class backup_history(models.Model):
    _name = 'kn.auto.backup_backup_history'
    _description = 'kn_auto_backup.kn_auto_backup_history'

    date = fields.Date(string="Date")
    db_name = fields.Char(string="Database's name")
    device = fields.Char(string="Deivice")
    file_name = fields.Char(string="File name")
    status = fields.Boolean(string="Status", required=True)
