{
	'name' : "STAMPITGO",
	'author' : "Techanipr",
	'version' : "1.0",
	'images' : 'images/mycmpaccnt.png',
	'category' : 'Merchant Sign Up Form',
	'depends' : ['base','base_setup','base_status','mail', 'resource','web_kanban'],
	# 'demo_xml' : [ 
	# 				'security/mycompany_security.xml',
	# 				'security/ir.model.access.csv',
	# 				'merchantform_view.xml',],
	# 'data' : ['wizard/test_wizard_view.xml',
	# 'mycompany_view.xml',
	# 'security/mycompany_security.xml',
	# 'security/ir.model.access.csv',
	# 'mycompany_workflow.xml',
	# 'mycompany_config_view.xml',
	# ],
	'data' : [  'security/merchant_security.xml',
				'security/ir.model.access.csv',
				'merchantform_view.xml',
			 ],
	'installable' : True,
	'auto_install' : False,
	'application' : True,
}