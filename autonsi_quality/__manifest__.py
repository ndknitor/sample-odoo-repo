# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    'name': 'Manufacturing, Work Order, Quality Control',
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Manufacturing",
    "license": "OPL-1",
    "summary": "Work order Quality Control, Analyze Product Quality Module,Manufacturing Product Quality Control,Quality Control for MRP, Quality Control for manufacturing,Product Quality Control,QC Validation,MRP QUALITY ASSURANCE,quality inspection alerts Odoo",
    "description": """Currently, in odoo, there are no options for 'Quality Control'. So, don't worry about that. Here we build a module that will help you to manage the quality of your products. Nowadays in the majority of businesses have Manufacturing, importing, exporting products. So you can receive goods(products) via transportation. Transportation increases the likelihood of goods being damaged. That's why you need to check product quality while you receiving or delivering products. Good quality control helps companies meet consumer demand with better products. This module will help you to analyze data of product quality checks.""",
    "version": "15.0.1",
    'depends': [
        'mail',
        'mrp',
        'hr',
        'autonsi_mmo'
    ],
    'data': [
        'security/sh_mrp_qc_security.xml',
        'security/ir.model.access.csv',
        'views/quality_team_view.xml',
        'views/mrp_all_operations.xml',
        # 'data/quality_alert_data.xml',
        # 'data/sequence.xml',
        'views/quality_alert_stage_view.xml',
        'views/quality_alert_tags.xml',
        'views/quality_point.xml',
        'views/qc_dashboard.xml',
        'views/mrp_production.xml',
        'views/mrp_masterproduction.xml',
        'views/mrp_quality_check.xml',
        'views/mes_qc_form.xml',
        'wizard/mes_qc_check_popup.xml',

        'wizard/mrp_quality_text_wizard.xml',
        'wizard/mrp_quality_pass_fail_wizard.xml',
        'wizard/mrp_pics_wizard.xml',
        'wizard/mrp_measurement_wizard.xml',
        'wizard/mrp_correct_measurement_wizard.xml',
        'wizard/mrp_qc_measurement_wizard.xml',
        'wizard/mrp_allow_qc_test.xml',
        'wizard/mrp_quality_check_report_wizard.xml',
        'report/mrp_qc_check_report.xml',
        'report/workorder_qc_check_report.xml',
        'report/mrp_quality_control_report_template.xml',
        'views/menu.xml',
        'views/mes_qc_form_web_template.xml'

    ],
    'assets': {
        'web.assets_backend': [
            'autonsi_quality/static/lib/codebase/suite.css',
            'autonsi_quality/static/lib/codebase/suite.js',
            'autonsi_quality/static/src/js/widget_qc_check.js',

        ],

        'web.assets_qweb': {
            'autonsi_quality/static/src/xml/mes_qc_check_template.xml',
        },
    },
    "images": ["static/description/background.png", ],
    "auto_install": False,
    "installable": True,
    "price": 100,
    "currency": "EUR"
}
