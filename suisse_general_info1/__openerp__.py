{
	'name':"Suisse Capital Asset Management Company SA General info",
	'version':"1.0",
	'author':"TechAnipr Pvt. Ltd.",
	'category':"Suisse Asset Management",
	'sequence':14,
	'description':"""
Suisse Capital Asset Management Company SA.
=============================================
        We guide you to manage your assets.
	""",
	'website':"http://www.suissecapitalamc.com",
	'depends' : ['base'],
	'images':[],
	'init_xml': [],
	'data': [
	        'suisse_general_info_sequence.xml',
		'suisse_asset_sequence.xml',
		#'suisse_workflow.xml',
		'suisse_client_general_information_view.xml',
		'client_investment_risk_profile_view.xml',
		'customer_aml_profile_view.xml',
		'individual_bank_opening_form_view.xml',
		'company_bank_acc_opening_view.xml',
		'suisse_asset_capital_view.xml',
                'suisse_document_checklist_view.xml',
                'verify_identity.xml',
                'SCAMC_agrmnt_view.xml',
				'data/mail_data.xml',
		'security/capital_security.xml',
		'security/ir.model.access.csv',
		
	],
	'installable':True,
        'auto_install':False,
	'application':True,	
	   
}
