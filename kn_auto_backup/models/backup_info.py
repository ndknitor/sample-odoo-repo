# -*- coding: utf-8 -*-
import base64
import os
import subprocess

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.service import db
from datetime import datetime
from odoo.tools import config
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import psycopg2
from psycopg2 import OperationalError

class backup_info(models.Model):
    _name = 'kn.auto.backup'
    _description = 'kn_auto_backup.kn_auto_backup'

    TERM_SELECTION = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    PLACE_SELECTION = [
        ('google_drive', 'Google Drive'),
        ('amazon_s3', 'Amazon S3'),
    ]
    dbhost = fields.Char(string="Server's IP", required=True)
    dbname = fields.Char(string="Database's name", required=True)
    dbuser = fields.Char(string="Database's Username", required=True)
    dbpassword = fields.Char(string="Database's Password", required=True)
    dbport = fields.Integer(string="Database's port", required=True, default=5432) 
    
    company = fields.Many2one('res.partner', required=True)
    date_of_use = fields.Date(string="Date of use")
    place = fields.Selection(selection=PLACE_SELECTION, string='Auto backup', required=True)
    last_backup = fields.Datetime(string="Last backup" , readonly=True)
    schedule = fields.Integer(string='Schedule (Hours)', required=True, default=1, min_value=1, max_value=24)
    term = fields.Selection(selection=TERM_SELECTION, string='Term', required=True)
    contract_amount =  fields.Char(string="Contract amount", required=True) #fields.One2many('sale.order',string="Contract amount")
    amount = fields.Float(string="Amount")
    customer_manager = fields.Many2one('res.partner',string="Customer manager")
    autorestore = fields.Boolean(string='Auto restore')
    status = fields.Boolean(string='Status', readonly=True)

    @api.constrains('schedule')
    def _check_schedule_range(self):
        for record in self:
            if record.schedule < 1 or record.schedule > 24:
                raise ValidationError("Schedule value must be between 1 and 24.")

    def scheduleTask(self):
        model = self.env['kn.auto.backup']
        records = model.search([])
        for record in records:
            self.perform_backup(record)

    def perform_backup(self,record):
        self.backup(record)
        return
        current_datetime = datetime.now()
        current_hour = current_datetime.hour
        current_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        if (record.last_backup == False) :
            record.write({
                'last_backup': current_datetime_str
            })
            self.backup(record)
            return
        difference = 0
        if (record.term == "daily") :
            difference = (current_datetime - record.last_backup).days
        elif (record.term == "weekly") :
            difference = (current_datetime - record.last_backup).days // 7
        elif (record.term == "monthly") :
            difference = (current_datetime.year - record.last_backup.year) * 12 + current_datetime.month - record.last_backup.month
        if (difference == 0 or current_hour != record.schedule) :
            return
        self.backup(record)

    def backup(self,record):
        file_name = record.dbname+"_" + get_date_string() +".dump"
        file_path = os.path.join("/tmp", file_name)

        self.postgres_backup(record, file_path)
        if (record.autorestore == True) :
            self.postgres_restore(record, file_path)
        if (record.place == "google_drive") :
            self.upload_google_drive(record,file_path)
        elif (record.place == "amazon_s3") :
            self.upload_amazon_s3(file_path)
        
        history = self.env['kn.auto.backup_backup_history']
        values = {
            'date': datetime.now(),
            'db_name': record.dbname,
            'device': "OK",
            'file_name': file_name,
            'status': True,
        }
        history.create(values)

        os.remove(file_path)


    def postgres_backup(self, record, path):
        backup_command = [
            "pg_dump", "--dbname=postgresql://"+ record.dbuser +":"+ record.dbpassword +"@" + record.dbhost + ":" + record.dbport.__str__() +"/" +record.dbname
        ]
        execute_command(backup_command, path)

    def postgres_restore(self, record, path) :
        dbname = os.path.basename(path).split('.')[0]

        db_params_create = {
            'host': record.dbhost, 
            'port': record.dbport.__str__(), 
            'user': record.dbuser, 
            'password': record.dbpassword, 
        }
        db_params_restore = {
            'host': record.dbhost, 
            'port': record.dbport.__str__(), 
            'user': record.dbuser, 
            'password': record.dbpassword, 
            'dbname': dbname,       
        }
        connection_create = None
        cursor_create = None
        connection_restore = None
        cursor_restore = None
        try:
            # Connect to the PostgreSQL server where you want to create the new database
            connection_create = psycopg2.connect(**db_params_create)

            # Create a cursor object for creating the new database
            cursor_create = connection_create.cursor()

            # SQL command to create a new database
            create_db_query = "CREATE DATABASE %s;"
            
            # Execute the SQL command to create the new database
            cursor_create.execute(create_db_query, (dbname,))

            # Commit the transaction for creating the new database
            connection_create.commit()

            print(f"Database '{dbname}' created successfully!")

            # Connect to the PostgreSQL server where you want to restore the dump file
            connection_restore = psycopg2.connect(**db_params_restore)

            # Create a cursor object for restoring data
            cursor_restore = connection_restore.cursor()

            # Read the contents of the dump file
            with open(path, 'r') as file:
                dump_data = file.read()

            # Execute the SQL commands to restore the database
            cursor_restore.execute(dump_data)

            # Commit the transaction for restoring data
            connection_restore.commit()

            print(f"Database '{dbname}' restored successfully from '{path}'")

        except (Exception, psycopg2.Error) as error:
            print(f"Error: {error}")

        finally:
            # Close the cursors and connections
            if cursor_create:
                cursor_create.close()
            if cursor_restore:
                cursor_restore.close()
            if connection_create:
                connection_create.close()
            if connection_restore:
                connection_restore.close()


    def is_postgres_alive(self, record):
        try:
            # Change these values to match your PostgreSQL server configuration
            connection = psycopg2.connect(
                host=record.dbhost,
                port=record.dbport,
                dbname=record.dbnamme
            )
            connection.close()
            return True
        except OperationalError as e:
            print("Error:", e)
            return False

    def upload_google_drive(self, record,file_path) :
        folderId = record.company.folder_id #self.env['ir.config_parameter'].sudo().get_param('kn_auto_backup.google_drive_access_token')
        if (folderId == None) :
            return
        credentials_path = os.path.join('/tmp', "service"+str(record.id)+".json")
        
        with open(credentials_path, 'wb') as f:
            f.write(base64.b64decode(record.company.service_file))

        credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://www.googleapis.com/auth/drive'])
        service = build('drive', 'v3', credentials=credentials)
        media = MediaFileUpload(file_path)
        file_name = os.path.basename(file_path)
        file_metadata = {
            'name': file_name,
            'parents': [folderId]
        }
        file = service.files().create(body=file_metadata, media_body=media, fields='id,name').execute()
        print(f"File '{file_name}' uploaded to Google Drive with ID: {file['id']}")
        os.remove(credentials_path)
        
        # folderId = self.env['ir.config_parameter'].sudo().get_param('kn_auto_backup.google_drive_access_token')
        # if (folderId == None) :
        #     return
        # credentials_path = os.path.join(get_module_path("kn_auto_backup"), "service.json")
        # credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://www.googleapis.com/auth/drive'])
        # service_account.Credentials.from_service_account_file()
        # service = build('drive', 'v3', credentials=credentials)
        # media = MediaFileUpload(file_path)
        # file_name = os.path.basename(file_path)
        # file_metadata = {
        #     'name': file_name,
        #     'parents': [folderId]
        # }
        # file = service.files().create(body=file_metadata, media_body=media, fields='id,name').execute()
        # print(f"File '{file_name}' uploaded to Google Drive with ID: {file['id']}")

    def upload_amazon_s3(self,db_name,file_path) :
        print("Dummy upload amazon s3 ")

def execute_command(command_args, output_file = None):
    try:
        if (output_file == None) :
            return subprocess.run(command_args, stderr=subprocess.PIPE, check=True).returncode
            # Open a binary file for writing the output
        with open(output_file, "wb") as output_handle:
            # Execute the command and capture its output
            result = subprocess.run(command_args, stdout=output_handle, stderr=subprocess.PIPE, check=True)
            # Return the command's return code
        return result.returncode
    except Exception as e:
        print(e)
    
def get_date_string():
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d-%h-%m-%s")
    return date_string

def get_module_path(module_name):
    addons_path = config.get('addons_path')
    module_path = False
    addons_paths = addons_path.split(',')
    for path in addons_paths:
        module_path_candidate = os.path.join(path.strip(), module_name)
        if os.path.isdir(module_path_candidate):
            module_path = module_path_candidate
            break
    return module_path