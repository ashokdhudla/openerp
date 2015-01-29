{
    'name': 'Royal Yachts Booking Module',
    'version': '1.0',
    'category': 'General',
    'description': """
This Application is used by RY in order to record each Yatch Booking and accounting application.
""",
    'author': 'Tech Anipr',
    'maintainer': 'Techanipr Pvt Ltd',
    'website': 'http://www.techanipr.com',
    'depends': ['base','sale','account_voucher','hr'],
    'data': [
    'security/ry_security.xml',
    'security/ir.model.access.csv',
	'ry_booking_sequence.xml',
	'ry_configuration_view.xml',
    'ry_config.xml',
    'yacht_booking_report.xml',
    'yacht_report.xml',
    # 'data/next_date.xml',
    'data/send_mail.xml',
    ],
    'installable': True,
    'auto_install': False,
    
}
