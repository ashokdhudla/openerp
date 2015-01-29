from openerp.osv import osv,fields
from openerp.tools.translate import _

class individual_bank_opening_form(osv.osv):
	_name = "individual.bank.opening.form"
	
	_columns = {
		'name':fields.char('Description',size=200,readonly=True),
		'name_company_financial_intermediary':fields.char('Name/Company name of the Financial intermediary',size=200),
	  ###  B1 fields  ###
		'contracting_party_title':fields.char('Title',size=100),
		'contracting_party_lastname_firstname':fields.char('Name/Company name(if appropiate)', size=50),
		'street_contracting_party': fields.char('Street', size=128),
        	'street2_contracting_party': fields.char('Street2', size=128),
        	'zip_contracting_party': fields.char('Postcode', change_default=True, size=24),
        	'city_contracting_party': fields.char('City', size=128),
        	'state_id_contracting_party': fields.many2one("res.country.state", 'State'),
		'contracting_party_country_domicile':fields.many2one('res.country', 'Country of Domicile'),
		'contracting_party_nationality':fields.many2one('res.country', 'Nationality'),
		'contracting_party_date_of_birth':fields.date('Date of birth'),
		###  B2 fields ###
		'is_beneficial_owner':fields.boolean('The contracting party is the sole beneficial owner of the assets.'),
		'is_not_beneficial_owner':fields.boolean('The contracting party is not the beneficial owner/sole beneficial owner of the assets.'),
		'beneficial_owner_lastname_firstname':fields.char('Lastname/Firstname'),
		'street_beneficial_owner': fields.char('Street', size=128),
        	'street2_beneficial_owner': fields.char('Street2', size=128),
        	'zip_beneficial_owner': fields.char('Postcode', change_default=True, size=24),
        	'city_beneficial_owner': fields.char('City', size=128),
        	'state_id_beneficial_owner': fields.many2one("res.country.state", 'State'),
		'beneficial_owner_country_domicile':fields.many2one('res.country', 'Country of Domicile'),
		'beneficial_owner_nationality':fields.many2one('res.country', 'Nationality'),
		'beneficial_owner_date_of_birth':fields.date('Date of birth'),
		'description_of_relation':fields.text('Description',size=255, help = '''If a power of attorney is being granted to a person who is clearly not in a sufficiently close relationship to the contracting party,please provide a description of the relationship of the account holder of the power of attorney'''),
		### B3 fields  ###
		'description_intermediary_relationship':fields.text('How was the relationship established?Duration of relationship?'),
		### C1 fields  ###
		'single_c1':fields.boolean('Single'),
		'married_c1':fields.boolean('Married'),
		'divorced_c1':fields.boolean('Divorced'),
		'seperated_c1':fields.boolean('Seperated'),
		'widowed_c1':fields.boolean('Widowed'),
		'spouse_name_c1':fields.char('Name of spouse/partner',size=50),
		'occupation_c1':fields.char('Occupation',size=20),
		'date_of_birth_c1':fields.date('Date of birth'),
		'children_yes_c1':fields.boolean('Yes'),
		'children_no_c1':fields.boolean('No'),
		'childre_personallyknown_c1':fields.boolean('Yes'),
		'childre_personallyknown_c1_one':fields.boolean('No'),
		'personal_background_c1':fields.one2many('individual.form.personal.background','children_id_c1','Personal Details'),
		'closerelation_info_c1':fields.text('Info about close relations'),
		'note_c1':fields.text('Note',size=100),
		## C2 Fields ##
		'self_employed_c2':fields.boolean('Self-employed'),
		'employed_c2':fields.boolean('Employed'),
		'retired_c2':fields.boolean('Retired'),
		'student_c2':fields.boolean('Student'),
		'not_gain_employed_c2':fields.boolean('Not gainfully employed'),
		'other_c2':fields.boolean('Other'),
		'occupation_desc_c2':fields.text('Client current/previous occcupation'),
		'public_fun_Y_c2':fields.boolean('Yes'),
		'public_fun_N_c2':fields.boolean('No'),
		'politics_c2':fields.boolean('Politics'),
		'church_c2':fields.boolean('Church'),
		'armed_forces_c2':fields.boolean('Armed forces'),
		'aristrocracy_c2':fields.boolean('Aristrocracy'),
		'other_c2':fields.boolean('Other'),
		'details_c2':fields.text('Please provide details'),
		## C3 Fields ##
		'other_keyinfo_c3':fields.text('Other key Info'),
		## D.1 Fields ##
		'assets_value_d1':fields.float('Current assets (total value)'),
		'bank_deposits_d1':fields.float('Bank deposits,securities'),
		'life_insurance_d1':fields.float('Life insurance'),
		'realestate_d1':fields.float('Real estate'),
		'asset_other_d1':fields.float('Other (e.g.stakes,collections etc.)'),
		'assets_details_d1':fields.char('(please provide details)'),
		'ubs_assets_d1':fields.float('Thereof assets held by UBS'),
		'assests_in_6to9mnths_d1':fields.float('Total assets by UBS in 6 to 9 months'),
		'income_situation_d1':fields.float('Income situation (estimate)'),
		'income_sources_d1':fields.char('Sources (e.g. salary,income from investments)'),
		'total_currentdebts_d1':fields.float('Total current debts'),
		'loans_mortgages_d1':fields.float('Loans, martgages etc.;'),
		'loan_details_d1':fields.char('(please provide details)'),
		'assets_acquire_desc_d1':fields.text('How client acquire his/her assets'),
		'gift_inheritance_d1':fields.boolean('Gift/inheritance'),
		'company_sale_d1':fields.boolean('Sale of company'),
		'income_salary_d1':fields.boolean('Income/salary'),
		'sale_proceeds_d1':fields.boolean('Proceeds from sales'),
		'sale_realestate_d1':fields.boolean('Sale of real estate'),
		'asset_source_other_d1':fields.boolean('Other'),
		'details_assets_d1':fields.text('In each please provide details'),
		'bank_transfer_d1':fields.boolean('Bank transfer'),
		'security_delivery_d1':fields.boolean('Delivery of securities'),
		'cash_deposit_d1':fields.boolean('Cash deposit'),
		'partial_delivery_d1':fields.boolean('Partial delivery'),
		'deliver_asset_other_d1':fields.boolean('Other'),
		'details_assets_delivery_d1':fields.text('If other provide details'),
		'name_d1':fields.char('Name (e.g.of bank)'),
		'location_d1':fields.many2one("res.country.state", 'Location'),
		'country_d1':fields.many2one('res.country', 'Country'),
		## Section F fields ##
		'ac2_title':fields.char('Title'),
		'ac2_firstname':fields.char('Firstname'),
		'ac2_companyname':fields.char('Lastname/company'),
		'street_ac2': fields.char('Street', size=128),
        	'street2_ac2': fields.char('Street2', size=128),
        	'zip_ac2': fields.char('Postcode', change_default=True, size=24),
        	'city_ac2': fields.char('City', size=128),
        	'state_id_ac2': fields.many2one("res.country.state", 'State'),
		'ac2_country_domicile':fields.many2one('res.country', 'Country of Domicile'),
		'ac2_nationality':fields.many2one('res.country', 'Nationality'),
		'ac2_date_of_birth':fields.date('Date of birth'),
		'ac2_date_of_incorporation':fields.date('Date of incorporation'),
		'ac3_title':fields.char('Title'),
		'ac3_firstname':fields.char('Firstname'),
		'ac3_companyname':fields.char('Lastname/company'),
		'street_ac3': fields.char('Street', size=128),
        	'street2_ac3': fields.char('Street2', size=128),
        	'zip_ac3': fields.char('Postcode', change_default=True, size=24),
        	'city_ac3': fields.char('City', size=128),
        	'state_id_ac3': fields.many2one("res.country.state", 'State'),
		'ac3_country_domicile':fields.many2one('res.country', 'Country of Domicile'),
		'ac3_nationality':fields.many2one('res.country', 'Nationality'),
		'ac3_date_of_birth':fields.date('Date of birth'),
		'ac3_date_of_incorporation':fields.date('Date of incorporation'),
		'ac4_title':fields.char('Title'),
		'ac4_firstname':fields.char('Firstname'),
		'ac4_companyname':fields.char('Lastname/company'),
		'street_ac4': fields.char('Street', size=128),
        	'street2_ac4': fields.char('Street2', size=128),
        	'zip_ac4': fields.char('Postcode', change_default=True, size=24),
        	'city_ac4': fields.char('City', size=128),
        	'state_id_ac4': fields.many2one("res.country.state", 'State'),
		'ac4_country_domicile':fields.many2one('res.country', 'Country of Domicile'),
		'ac4_nationality':fields.many2one('res.country', 'Nationality'),
		'ac4_date_of_birth':fields.date('Date of birth'),
		'ac4_date_of_incorporation':fields.date('Date of incorporation'),
		## Section G fields ##
		'place_g1':fields.char('Place'),
		'date_g1':fields.date('Date'),
		'sign_g1':fields.char('Signature of delegated employee of the financial intermediary'),
	}
	_defaults={
		'name':'Individual Bank Opening Form',
	}
	_order = 'contracting_party_title'
	
individual_bank_opening_form()

class  individual_form_personal_background(osv.osv):
	_columns = {
		'name_of_children_c1':fields.char('Name(s) of Children'),
		'children_occupation_c1':fields.char('Occupation', change_default=True),
		'children_dof_c1':fields.date('Date of Birth', change_default=True),
		'children_id_c1':fields.many2one('individual.bank.opening.form','Children', select=True, ondelete='cascade'),
	}

	
	_name = 'individual.form.personal.background'
	_description = 'Personal Background Children'

individual_form_personal_background()

