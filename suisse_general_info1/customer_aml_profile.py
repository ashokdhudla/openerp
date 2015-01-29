from openerp.osv import osv,fields

class customer_aml_profile(osv.osv):
	_name="customer.aml.profile"
	_columns={
	'name':fields.char('Description',size=80,readonly=True),
	'customerno':fields.integer('Customer no./AML file No.'),
	'form_filled_name':fields.char('Form was completed by'),
	'AML_date':fields.date('Start of AML mandate(date):'),
	'individual_name_firstname':fields.char('Name/firstname'),
	'company_name':fields.char('Name of Company'),
	'individual_date_of_birth':fields.date('Date of birth'),
	'established_date':fields.date('Date of establishment'),
	'street_individual': fields.char('Street', size=128),
        'street2_individual': fields.char('Street2', size=128),
        'zip_individual': fields.char('Postcode', change_default=True, size=24),
        'city_individual': fields.char('City', size=128),
        'state_id_individual': fields.many2one("res.country.state", 'State'),
        'country_id_individual': fields.many2one('res.country', 'Country'),
	'street_legalperson': fields.char('Street', size=128),
        'street2_legalperson': fields.char('Street2', size=128),
        'zip_legalperson': fields.char('Postcode', change_default=True, size=24),
        'city_legalperson': fields.char('City', size=128),
        'state_id_legalperson': fields.many2one("res.country.state", 'State'),
        'country_id_legalperson': fields.many2one('res.country', 'Country'),
	'party_nationality':fields.many2one('res.country', 'Nationality'),
	'purpose':fields.char('Purpose'),
	'individual_phno':fields.char('Phone no.'),
	'legalperson_phno':fields.char('Phone no.'),
	'individual_email':fields.char('Email'),
	'legalperson_email':fields.char('Email'),
	'is_party_to_benefiacialownerY':fields.boolean('Yes-If Yes,details from section 3 required'),
	'is_party_to_benefiacialownerN':fields.boolean('No-If No,details from parametric.2 required(+form.no3 is required)'),
	'beneficialowner_name':fields.char('Name/firstname'),
	'beneficialowner_dob':fields.date('Date of birth'),
	'street_beneficialowner': fields.char('Street', size=128),
        'street2_beneficialowner': fields.char('Street2', size=128),
        'zip_beneficialowner': fields.char('Postcode', change_default=True, size=24),
        'city_beneficialowner': fields.char('City', size=128),
        'state_id_beneficialowner': fields.many2one("res.country.state", 'State'),
        'country_id_beneficialowner': fields.many2one('res.country', 'Country'),
	'beneficialowner_nationality':fields.many2one('res.country', 'Nationality'),
	'financial_intermediary':fields.text('Contract to the financial intermediary'),
	'beneficialowner_occupation':fields.char('Ocuupation/resp.business activities'),
	'business_activities':fields.char('Prev.professional/business activities'),
	'income_lt300000CHF':fields.boolean("<300'000CHF"),
	'income_300000-1millionCHF':fields.boolean("300'000CHF - 1 million CHF"),
	'income_gt1millionCHF':fields.boolean(">1 million CHF"),
	'netasset_lt1millionCHF':fields.boolean('<1 million CHF'),
	'netasset_1-5millionCHF':fields.boolean('1-5 million CHF'),
	'netasset_gt5millionCHF':fields.boolean('>5 million CHF'),
	"planned_transactions_lt500'000CHF":fields.boolean("<500'000 CHF"),
	"planned_transactions_500'000-2millionCHF":fields.boolean("500'000-2 million CHF"),
	"planned_transactions_gt2millionCHF":fields.boolean(">2 million CHF"),
	"planned_transactions_unknown":fields.boolean("Unknown"),
	'remarks':fields.char('Remarks'),
	'funds_info':fields.text('Info about Amount,source of funds'),
	'is_PEP':fields.boolean('Party/beneficial owner is a PEP(polotically exposed person,para.1.4.,Lit.B.SRO Regs.)'),
	'geo_criterion':fields.boolean('Geographical criterion:NCCT(=non cooperarive countries and territories).www.fatf-gafi.org'),
	'new_unknown':fields.boolean('New,unknown customer without personal contact'),
	'your_criteria':fields.boolean('Your criteria for higher risk relationships(created by FI-please explain briefly below)'),
	'possible_explanations':fields.text('Possible Explanations'),
	'none':fields.boolean('None of the above-mentioned variants to meet'),
	'relevance_info':fields.text('Info of relevance'),
	'reasons_to_hire':fields.text('Reasons party,respectively.the beneficial owner in person to/us to hire me?'),
	'further_comments':fields.text('Further Comments'),
	'date1':fields.date('Date'),
	'comments':fields.text('Comments'),
	'sign1':fields.char('Signature'),
	'date2':fields.date('Date'),
	'additional_comments':fields.char('Additional comments',size=200),
	'sign2':fields.char('Signature')
	}
	_defaults={
		'name':'Opening AML-FIle/Customer Profile',
	}
	_order = 'customerno'

customer_aml_profile()
	