{
    'name': 'Troubleshoot Module For Tech Anipr',
    'version': '1.0',
    'category': 'Troubleshoot',
    'description': """
Troubleshoot Module For Tech Anipr ERP. It will help ERP team to Better manage ERP.
and Help our Company to get rid of Any Problem related to ERP.

===================================================
""",
    'author': 'Deepak Nayak',
    'maintainer': 'Techanipr Pvt Ltd',
    'website': 'http://www.techanipr.com',
    'depends': ['base'],
    'data': [
        'TA_troubleshoot_view.xml',
        'security/troubleshoot_security.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
    
}
