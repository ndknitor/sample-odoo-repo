import psycopg2
from odoo import models, fields

class server_history(models.Model):
    _name = 'kn.auto.backup_server_history'
    _description = 'kn_auto_backup.kn_auto_backup_server_history'

    date = fields.Date(string="Date")
    name = fields.Char(string="Server's host")
    status = fields.Boolean(string="Status")
    description = fields.Char(string="Description")

    def scheduleTask(self):
        backup_records = self.env['kn.auto.backup'].search([])
        if not backup_records:
            return
        
        grouped_data = backup_records.read_group(
            domain=[],
            fields=['dbhost', 'dbport', 'dbuser', 'dbpassword'],
            groupby=['dbhost'],
        )

        for group in grouped_data:
            dbhost = group['dbhost']
            status = self.check_server(group)
            values = {
                'date': fields.Date.today(),
                'name': dbhost,
                'status': status,
                'description': "OK" if status else "Down",
            }
            self.create(values)

    def check_server(self, record):
        try:
            # Attempt to connect to the PostgreSQL server
            conn = psycopg2.connect(
                host=record['dbhost'],
                port=record['dbport']
            )
            # If the connection is successful, the server is alive
            print("PostgreSQL server is alive!")
            conn.close()
            return True

        except psycopg2.OperationalError as e:
            # If there's an error, the server is not alive
            print("PostgreSQL server is not alive:", e)
            return False 