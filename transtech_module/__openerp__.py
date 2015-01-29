{
    'name': 'Transtech Module',
    'version': '1.0',
    'category': 'General',
    'description': """
This Application is used By Transtech for recording the services provided
by their team which help them to work efficiently and provide the transparency.
""",
    'author': 'Tech Anipr',
    'maintainer': 'Techanipr Pvt Ltd',
    'website': 'http://www.techanipr.com',
    'depends': ['base','board','mail'],
    'data': [
        'wizard/atm_move_view.xml',
		'security/transtech_atm_updater_security_view.xml',
        'security/ir.model.access.csv',
		'transtech_atm_sequence.xml',
		'transtech_atm_sequence.xml',
        'configuration_panel_view.xml',
		'transtech_atm_setup_view.xml',
		'transtech_customer_setup_view.xml',
		'transtech_surveys_management.xml',
		'transtech_alert_view.xml',
		'transtech_atm_dashboard.xml',
        'survey_details_view.xml',
	    'transtech_site_inspection_view.xml',
        'report/transtech_survey_task_report.rml',
        'transtech_surveys_report.xml',
        'internal_alerts_view.xml',
        'dashboard_alerts.xml',
        'task_done_dashboard.xml',
        'data/mail_data.xml',
    ],
    'web': True,
    'js': [
           'static/src/js/gmap.js',
           'static/src/js/gmap_rental.js',
        ],
    'css': [
        'static/src/css/gmap.css', 
        'static/src/css/gmap_rental.css', 
        ],
    'qweb': [
            'static/src/xml/base.xml',
            'static/src/xml/base_rental.xml',
         ],
    'installable': True,
    'auto_install': False,
    
}
