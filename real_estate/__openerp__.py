{
	'name' : 'Real Estate Crm',
	'version' : '1.0',
	'author' : 'Anipr Technology',
	'category' : 'Real estate',
	'maintainer' : 'Anipr Technology',
	'website' : 'www.anipr.com',
	'description' : """
Crm for Real estate.
====================
	""",
	'depends' : ['base'],
	'data' : [	
				'wizard/add_images_view.xml',
				'security/real_estate_security.xml',
				'security/ir.model.access.csv',
				'real_estate_view.xml',
				'real_estate_sequence.xml',
				'real_estate_sales_view.xml',
				],
	'web': True,
    'js': [
           'static/src/js/gmap.js',
        ],
    'css': ['static/src/css/gmap.css', ],
    'qweb': ['static/src/xml/base.xml', ],
	'installable' : True,
	'auto_install' : False,
	'application' : True,
}