{
	'name' : "Transtech Img",
	'author' : "anipr technology",
	'version' : "1.0",
	'images' : 'images/mycmpaccnt.png',
	'category' : 'Transtech Form',
	'depends' : ['base'],
	'data' : [  
				'security/trans_cus_security.xml',
				'security/ir.model.access.csv',
				'transtech_multimg_view.xml',
			 ],
	'installable' : True,
	'auto_install' : False,
	'application' : True,
}