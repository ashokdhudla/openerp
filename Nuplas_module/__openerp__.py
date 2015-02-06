{
    'name': 'Nuplas Industries Module',
    'version': '1.0',
    'category': 'General',
    'description': """
This Application is used by Nuplas Industries for print their label and Keep track of 
their packaging process.
""",
    'author': 'Tech Anipr',
    'maintainer': 'Techanipr Pvt Ltd',
    'website': 'http://www.techanipr.com',
    'depends': ['base','product','label'],
    'data': [
        'wizard/label_print_wizard_view.xml',
        # 'nuplas_packaging_sequence.xml',
        'security/nuplas_security.xml',
        'security/ir.model.access.csv',
        'nuplas_configuration_view.xml',
        'label_size_data.xml',
        'label_report.xml',
        # 'work_order_report_view.xml',
		
    ],

    'web': True,
    'js': [
           'static/src/js/nuplas.js',
        ],
    'installable': True,
    'auto_install': False,
    
}
