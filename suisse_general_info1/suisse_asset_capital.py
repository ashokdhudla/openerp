import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

class suisse_capital_client_form(osv.osv):
	_name = "suisse.capital.client.form"
	
	STATE_SELECTION = [
		('sectiona', 'Section A/B'),
		('sectionb', 'Section C.1'),
		('sectionc', 'Section C.2'),
		('sectionc_1', 'Section C.3'),
		('sectionc_2', 'Section C.4'),
		('sectionc_2_1','Section C.4.1'),
		('confirmed', 'Waiting Approval'),
		('sectiond_1', 'Section D.1'),
		('sectiond_1_1', 'Section D.2'),
		('sectiond_2', 'Section D.3'),
		('sectiond_3', 'Section D.3.1'),
		('sectione', 'Section E'),
		('approved', 'Approved'),
		('cancel', 'Cancelled')
	]
	
	_columns = {
		'name':fields.char('CIN Number',required=True,readonly=True,select=True,help="Unique key per client"),
		'name_contract':fields.char('Name of the Contract',size=200,required=True,select=True,help="Name of the contract"),
		'name_client':fields.char('Client',size=200,required=True,help="Name of the client",select=True),
		'name_client_joint':fields.char('Second Client',size=200,help="Name of the second client",select=True),
		'policy_number':fields.char('Policy Number',help="if this is an application for an additional investment or premium,please provide your existing policy number.You can find this in your policy documentation",select=True),
		'is_company': fields.boolean('Is a Company', help="Check if the client is a company, otherwise it is a individual"),
		'is_joint': fields.boolean('Is a Joint', help="Check if the client is a Joint , otherwise it is a individual"),
		'pep_client':fields.text('Politically Exposed Person(PEP)',
			help="If any client come under PEP then write its detail here."
			
			),
		'user_id': fields.many2one('res.users', 'Creater', select=True, track_visibility='onchange'),
		'state': fields.selection(STATE_SELECTION, 'Status', readonly=True, track_visibility='onchange',
            help="Gives the status of the KYC Form ", select=True),
		'suisse_bank_account':fields.one2many('suisse.capital.bank.account.multi','suisse_capital_bank','Existing Bank Account'),
		'active': fields.boolean('Active', help="The active field allows you to hide the category without removing it."),
		'date_create':fields.date('Date', required=True, readonly=True, select=True),

		#Fields for Section C.1
		'bank_accountholder':fields.char('Name of the Account Holder',select=True,states={'sectionb': [('required', True)]}),
		'bank_account_number':fields.integer('Bank Account Number/IBAN*',select=True,size=18,states={'sectionb': [('required', True)]}),
		'sort_code':fields.char('Sort Code**',size=8),
		'swift_bic_code':fields.char('SWIFT or BIC CODE**',size=11),
		'bank_name_sectionc':fields.char('Bank Name',select=True,states={'sectionb': [('required', True)]}),
		'street_sectionc': fields.char('Street', size=128),
        	'street2_sectionc': fields.char('Street2', size=128),
        	'zip_sectionc': fields.char('PostCode', change_default=True, size=24),
        	'city_sectionc': fields.char('City', size=128),
        	'state_id_sectionc': fields.many2one("res.country.state", 'State'),
       		'country_id_sectionc': fields.many2one('res.country', 'Country'),
        	'period_of_trust':fields.date('Period of Trust', select=True,states={'sectionb': [('required', True)]}),

		#Fields for Section C.2
		'occupation_c2one':fields.char('Occupation',select=True,states={'sectionc': [('required',True)]}),
		'name_of_employer_c2one':fields.char('Name of employer',select=True,states={'sectionc': [('required',True)]}),
		'street_sectionc2_c2one': fields.char('Street', size=128),
        	'street2_sectionc2_c2one': fields.char('Street2', size=128),
        	'zip_sectionc2_c2one': fields.char('PostCode', change_default=True, size=24),
        	'city_sectionc2_c2one': fields.char('City', size=128),
      	 	'state_id_sectionc2_c2one': fields.many2one("res.country.state", 'State'),
        	'country_id_sectionc2_c2one': fields.many2one('res.country', 'Country'),
		# Fields for Section C.2 for client 2
		'occupation_c2two':fields.char('Occupation',select=True,states={'sectionc':[('required',True)]}),
		'name_of_employer_c2two':fields.char('Name of employer',select=True,states={'sectionc':[('required',True)]}),
		'street_sectionc2_c2two': fields.char('Street', size=128),
        	'street2_sectionc2_c2two': fields.char('Street2', size=128),
        	'zip_sectionc2_c2two': fields.char('PostCode', change_default=True, size=24),
        	'city_sectionc2_c2two': fields.char('City', size=128),
      	 	'state_id_sectionc2_c2two': fields.many2one("res.country.state", 'State'),
        	'country_id_sectionc2_c2two': fields.many2one('res.country', 'Country'),

		# Fields for Section C.3 
		'currency_sectioncthree':fields.many2one('res.currency','Currency',select=True),
		'amount_sectioncthree':fields.char('Amount',select=True),

		# Fields for Section C.4.1
		'income_from_employment':fields.boolean('Income from Employment'),
		'income_from_your_business':fields.boolean('Income from your buisness'),
		'currency_one':fields.many2one('res.currency','Currency',select=True),
		'gross_salary':fields.integer('Gross Salary'),
		'bonus':fields.integer('Bonus (if any)',select=True),
		'website_one':fields.char('Website Address'),
		#Origin wealth two
		'income_from_your_business_two':fields.boolean('Income from your buisness'),
		'currency_two':fields.many2one('res.currency','Currency',select=True),
		'total_gross_income_two':fields.integer('Total gross income/profits'),
		'website_two':fields.char('Website Address'),
		#Origin wealth three
		'unearned_income':fields.boolean('Other Unearned Income'),
		'nature_of_income':fields.char('Nature of Income',select=True),
		'currency_three':fields.many2one('res.currency','Currency',select=True),
		'amount_three':fields.integer('Amount'),
		'date_received':fields.date('Date Received'),
		#Origin wealth four
		'investment_saving':fields.boolean('Investment/Savings'),
		'currency_four':fields.many2one('res.currency','Currency',select=True),
		'amount_four':fields.integer('Amount'),
		'length_investments':fields.char('Length of Investments/Savings',select=True),
		'yes':fields.boolean('Yes'),
		'no':fields.boolean('No'),
		'name_of_account_holder':fields.char('Name of Account Holder'),
		'account_number':fields.integer('Account Number',select=True),
		'financial_bank':fields.char('Name of Financial institution/bank'),
		#Origin wealth five
		'maturing_investment':fields.boolean('Maturing investments/Policy claim/Replacement policy'),
		'name_company_five':fields.char('Name of Company',select=True),
		'person_held_policy':fields.char('Name of the person who held the policy'),
		'reason_policy':fields.text('Reason for policy claim or replacement policy'),
		'currency_five':fields.many2one('res.currency','Currency',select=True),
		'amount_five':fields.integer('Amount'),
		'penalty_incurred':fields.integer('Surrender Penalty incurred (if any )'),
		'date_received_five':fields.date('Date Received',select=True),
		'length_policy':fields.char('Length of investment/policy'),
		#Origin wealth Six
		'sale_of_property':fields.boolean('Sale of property'),
		'street_six': fields.char('Street', size=128),
        	'street2_six': fields.char('Street2', size=128),
        	'zip_six': fields.char('PostCode', change_default=True, size=24),
        	'city_six': fields.char('City', size=128),
        	'state_id_six': fields.many2one("res.country.state", 'State'),
        	'country_id_six': fields.many2one('res.country', 'Country'),
		'currency_six':fields.many2one('res.currency','Currency',select=True),
		'amount_six':fields.integer('Amount',),
		'date_sale':fields.date('Date of sale',select=True),
		#Origin wealth Seven
		'sale_of_interest_company':fields.boolean('Sale of interest in a company'),
		'name_company_seven':fields.char('Name of the Company',select=True),
		'street_seven': fields.char('Street', size=128),
        	'street2_seven': fields.char('Street2', size=128),
        	'zip_seven': fields.char('PostCode', change_default=True, size=24),
        	'city_seven': fields.char('City', size=128),
        	'state_id_seven': fields.many2one("res.country.state", 'State'),
        	'country_id_seven': fields.many2one('res.country', 'Country'),
		'nature_of_buisness':fields.char('Nature of Buisness'),
		'currency_seven':fields.many2one('res.currency','Currency',select=True),
		'amount_seven':fields.integer('Amount'),
		'date_sale_interest':fields.date('Date of sale',select=True),

		#Origin wealth Eight
		'sale_of_shares':fields.boolean('Sale of shares'),
		'des_share_sold':fields.text('Description of shares sold',select=True),
		'how_sold_eight':fields.char('How were they sold?',size=200),
		'name_company_share_held':fields.char('Name of the Company'),
		'street_eight': fields.char('Street', size=128),
        	'street2_eight': fields.char('Street2', size=128),
        	'zip_eight': fields.char('PostCode', change_default=True, size=24),
        	'city_eight': fields.char('City', size=128),
        	'state_id_eight': fields.many2one("res.country.state", 'State'),
        	'country_id_eight': fields.many2one('res.country', 'Country'),
		'currency_eight':fields.many2one('res.currency','Currency',select=True),
		'amount_eight':fields.integer('Amount'),
		'date_of_sale_eight':fields.date('Date of sale',select=True),
		'len_holding_share':fields.char('Length of holding the share'),
		#Origin wealth nine
		'inheritance':fields.boolean('Inheritance'),
		'from_whom_nine':fields.char('From Whom',select=True),
		'relationship_to_person':fields.char('Your relationship to the person',size=200),
		'detail_inherited':fields.text('Details of exactly what was inherited'),
		'currency_nine':fields.many2one('res.currency','Currency',select=True),
		'amount_nine':fields.integer('Amount'),
		'date_received_nine':fields.date('Date received',select=True),
		#Origin wealth Tenth
		'loan':fields.boolean('Loan'),
		'name_provider':fields.char('Name of the loan provider',select=True),
		'street_ten': fields.char('Street', size=128),
        	'street2_ten': fields.char('Street2', size=128),
        	'zip_ten': fields.char('PostCode', change_default=True, size=24),
        	'city_ten': fields.char('City', size=128),
        	'state_id_ten': fields.many2one("res.country.state", 'State'),
        	'country_id_ten': fields.many2one('res.country', 'Country'),
		'reason_loan':fields.text('Reason for Loan'),
		'currency_ten':fields.many2one('res.currency','Currency',select=True),
		'amount_ten':fields.integer('Amount'),
		'date_of_loan':fields.date('Date of sale',select=True),
		#Origin wealth Eleventh
		'gift':fields.boolean('Gift'),
		'from_whom_eleven':fields.char('From whom',select=True),
		'relationship_applicant':fields.char('Relationship to applicant',select=True),
		'origin_of_wealth':fields.char('Origin of Wealth'),
		'reason_for_gift':fields.text('Reason for gift'),
		'currency_eleven':fields.many2one('res.currency','Currency',select=True),
		'amount_eleven':fields.integer('Amount'),
		'date_of_gift':fields.date('Date Received',select=True),
		#Origin wealth Twelveth
		'compensation':fields.boolean('Compensation'),
		'from_whom_comp':fields.char('From whom',select=True),
		'reason_for_comp':fields.text('Reason for Compensation'),
		'currency_twelve':fields.many2one('res.currency','Currency',select=True),
		'amount_twelve':fields.integer('Amount'),
		'date_of_comp':fields.date('Date Received',select=True),
		#Origin wealth Thirteen
		'competition':fields.boolean('Competition or gambling win'),
		'where_you_win':fields.text('Where and how did you win this money?',select=True),
		'organisation_paid_you':fields.char('Which organisation or Company paid you the prize money?'),
		'currency_thirteen':fields.many2one('res.currency','Currency',select=True),
		'amount_thirteen':fields.integer('Amount'),
		'date_of_win':fields.date('Date of win',select=True),
		#Origin wealth Fourteen
		'other':fields.boolean('Other'),
		'other_origin_wealth':fields.char('Origin of wealth',select=True),
		'description':fields.text('Description'),
		'currency_fourteen':fields.many2one('res.currency','Currency',select=True),
		'amount_fourteen':fields.integer('Amount'),
		'date_of_other':fields.date('Date Received',select=True),
		'document_evidence':fields.text("Please enter the documentary evidence\n\n that you are enclosing with your application\n\n"\
				"and KYC forms."
			),

		#Verification of client identity
		#Fields For Section D.1.1 Proof of identity

		#Proof of identity 1
		'name_id_sectiondone':fields.char('1.Name',select=True),
		'capacity_sectiondone':fields.char('Capacity',select=True),
		'passport_sectiondone':fields.boolean('Passport'),
		'nic_sectiondone':fields.boolean('National identity Card'),
		'doc_ref_sectiondone':fields.char('Document reference',select=True),
		#Proof of identity 2
		'name_id_sectiondtwo':fields.char('2.Name',select=True),
		'capacity_sectiondtwo':fields.char('Capacity',select=True),
		'passport_sectiondtwo':fields.boolean('Passport'),
		'nic_sectiondtwo':fields.boolean('National identity Card'),
		'doc_ref_sectiondtwo':fields.char('Document reference',select=True),
		#Proof of identity 3
		'name_id_sectiondthree':fields.char('3.Name',select=True),
		'capacity_sectiondthree':fields.char('Capacity',select=True),
		'passport_sectiondthree':fields.boolean('Passport'),
		'nic_sectiondthree':fields.boolean('National identity Card'),
		'doc_ref_sectiondthree':fields.char('Document reference',select=True),
		#Proof of identity 4
		'name_id_sectiondfour':fields.char('4.Name',select=True),
		'capacity_sectiondfour':fields.char('Capacity',select=True),
		'passport_sectiondfour':fields.boolean('Passport'),
		'nic_sectiondfour':fields.boolean('National identity Card'),
		'doc_ref_sectiondfour':fields.char('Document reference',select=True),
		#Proof of identity 5
		'name_id_sectiondfive':fields.char('5.Name',select=True),
		'capacity_sectiondfive':fields.char('Capacity',select=True),
		'passport_sectiondfive':fields.boolean('Passport'),
		'nic_sectiondfive':fields.boolean('National identity Card'),
		'doc_ref_sectiondfive':fields.char('Document reference',select=True),
		#Proof of identity 6
		'name_id_sectiondsix':fields.char('6.Name',select=True),
		'capacity_sectiondsix':fields.char('Capacity',select=True),
		'passport_sectiondsix':fields.boolean('Passport'),
		'nic_sectiondsix':fields.boolean('National identity Card'),
		'doc_ref_sectiondsix':fields.char('Document reference',select=True),
		
                #Connected Party Section D.1
                'connected_party_reason':fields.text("Name of Connected party and the reasons for connection"),
		'unaviable_document':fields.text("Unavailable documents and their reasons"),
		#Fields for Section D.1.2
		'recent_tax_bill':fields.char('Recent Bill'),
                'first_person_one':fields.boolean('1'),
		'second_person_one':fields.boolean('2'),
		'third_person_one':fields.boolean('3'),
		'four_person_one':fields.boolean('4'),
		'five_person_one':fields.boolean('5'),
		'six_person_one':fields.boolean('6'),
		'recent_mortage':fields.char('Recent Mortage'),
		'first_person_two':fields.boolean('1'),
		'second_person_two':fields.boolean('2'),    
                'third_person_two':fields.boolean('3'), 
		'four_person_two':fields.boolean('4'),
		'five_person_two':fields.boolean('5'),
		'six_person_two':fields.boolean('6'),
		'extract_elector':fields.char('Extract Elector'),
		'first_person_three':fields.boolean('1'),
		'second_person_three':fields.boolean('2'),    
                'third_person_three':fields.boolean('3'), 
		'four_person_three':fields.boolean('4'),
		'five_person_three':fields.boolean('5'),
		'six_person_three':fields.boolean('6'),
		'pension_document_state':fields.char('State Pension Document'),
		'first_person_four':fields.boolean('1'),
		'second_person_four':fields.boolean('2'),    
                'third_person_four':fields.boolean('3'), 
		'four_person_four':fields.boolean('4'),
		'five_person_four':fields.boolean('5'),
		'six_person_four':fields.boolean('6'),
		'recent_tax_doc':fields.char('Recent tax Document'),
		'first_person_five':fields.boolean('1'),
		'second_person_five':fields.boolean('2'),    
                'third_person_five':fields.boolean('3'), 
		'four_person_five':fields.boolean('4'),
		'five_person_five':fields.boolean('5'),
		'six_person_five':fields.boolean('6'),
		'recent_account_bank':fields.char('Recent Bank Account'),
		'first_person_six':fields.boolean('1'),
		'second_person_six':fields.boolean('2'),    
                'third_person_six':fields.boolean('3'), 
		'four_person_six':fields.boolean('4'),
		'five_person_six':fields.boolean('5'),
		'six_person_six':fields.boolean('6'),
		'proof_own_address':fields.char('Proof of Address'),
		'first_person_seven':fields.boolean('1'),
		'second_person_seven':fields.boolean('2'),    
                'third_person_seven':fields.boolean('3'), 
		'four_person_seven':fields.boolean('4'),
		'five_person_seven':fields.boolean('5'),
		'six_person_seven':fields.boolean('6'),
		'landline_entry':fields.char('Local Telephone Directory'),
		'first_person_eight':fields.boolean('1'),
		'second_person_eight':fields.boolean('2'),    
                'third_person_eight':fields.boolean('3'), 
		'four_person_eight':fields.boolean('4'),
		'five_person_eight':fields.boolean('5'),
		'six_person_eight':fields.boolean('6'),
		 #Fields for Section D.2
		'point_d2one':fields.boolean('Point One'),
		'point_d2two':fields.boolean('Point Two'),
		'point_d2three':fields.boolean('Point three'),
		'point_d2four':fields.boolean('Point four'),
		'point_d2five':fields.boolean('Point five'),
		'point_d2six':fields.boolean('Point Six'),
		'point_d2seven':fields.boolean('Point seven'),
		'point_d2eight':fields.boolean('Point eight'),
                 #Fields for Section D.3 Individual trustee
		'point_d3one':fields.boolean(''),
		'point_d3two':fields.boolean(''),
		'point_d3three':fields.boolean(''),
		'point_d3four':fields.boolean(''),
		# Fields for Individual trustee 1
		'settlor_donord3one':fields.boolean('Settlor/Donor'),
		'protector_d3one':fields.boolean('Protector'),
		'beneficiary_d3one':fields.boolean('Beneficiary'),
		'name_d3one':fields.char('Name',select=True),
		'birth_death_d3one':fields.date('Date of Birth or Death'),
		'birth_d3one':fields.boolean('Birth'),
		'death_d3one':fields.boolean('Death'),
		'street_d3one': fields.char('Street', size=128),
        	'street2_d3one': fields.char('Street2', size=128),
        	'zip_d3one': fields.char('PostCode', change_default=True, size=24),
        	'city_d3one': fields.char('City', size=128),
        	'state_id_d3one': fields.many2one("res.country.state", 'State'),
       		'country_id_d3one': fields.many2one('res.country', 'Country'),
		# Fields for Individual trustee 2
		'settlor_donord3two':fields.boolean('Settlor/Donor'),
		'protector_d3two':fields.boolean('Protector'),
		'beneficiary_d3two':fields.boolean('Beneficiary'),
		'name_d3two':fields.char('Name',select=True),
		'birth_death_d3two':fields.date('Date of Birth or Death'),
		'birth_d3two':fields.boolean('Birth'),
		'death_d3two':fields.boolean('Death'),
		'street_d3two': fields.char('Street', size=128),
        	'street2_d3two': fields.char('Street2', size=128),
        	'zip_d3two': fields.char('PostCode', change_default=True, size=24),
        	'city_d3two': fields.char('City', size=128),
        	'state_id_d3two': fields.many2one("res.country.state", 'State'),
       		'country_id_d3two': fields.many2one('res.country', 'Country'),
		# Fields for Individual trustee 3
		'settlor_donord3three':fields.boolean('Settlor/Donor'),
		'protector_d3three':fields.boolean('Protector'),
		'beneficiary_d3three':fields.boolean('Beneficiary'),
		'name_d3three':fields.char('Name',select=True),
		'birth_death_d3three':fields.date('Date of Birth or Death'),
		'birth_d3three':fields.boolean('Birth'),
		'death_d3three':fields.boolean('Death'),
		'street_d3three': fields.char('Street', size=128),
        	'street2_d3three': fields.char('Street2', size=128),
        	'zip_d3three': fields.char('PostCode', change_default=True, size=24),
        	'city_d3three': fields.char('City', size=128),
        	'state_id_d3three': fields.many2one("res.country.state", 'State'),
       		'country_id_d3three': fields.many2one('res.country', 'Country'),
		# Fields for Individual trustee 4
		'settlor_donord3four':fields.boolean('Settlor/Donor'),
		'protector_d3four':fields.boolean('Protector'),
		'beneficiary_d3four':fields.boolean('Beneficiary'),
		'name_d3four':fields.char('Name',select=True),
		'birth_death_d3four':fields.date('Date of Birth or Death'),
		'birth_d3four':fields.boolean('Birth'),
		'death_d3four':fields.boolean('Death'),
		'street_d3four': fields.char('Street', size=128),
        	'street2_d3four': fields.char('Street2', size=128),
        	'zip_d3four': fields.char('PostCode', change_default=True, size=24),
        	'city_d3four': fields.char('City', size=128),
        	'state_id_d3four': fields.many2one("res.country.state", 'State'),
       		'country_id_d3four': fields.many2one('res.country', 'Country'),
		# Fields for Individual trustee 5
		'settlor_donord3five':fields.boolean('Settlor/Donor'),
		'protector_d3five':fields.boolean('Protector'),
		'beneficiary_d3five':fields.boolean('Beneficiary'),
		'name_d3five':fields.char('Name',select=True),
		'birth_death_d3five':fields.date('Date of Birth or Death'),
		'birth_d3five':fields.boolean('Birth'),
		'death_d3five':fields.boolean('Death'),
		'street_d3five': fields.char('Street', size=128),
        	'street2_d3five': fields.char('Street2', size=128),
        	'zip_d3five': fields.char('PostCode', change_default=True, size=24),
        	'city_d3five': fields.char('City', size=128),
        	'state_id_d3five': fields.many2one("res.country.state", 'State'),
       		'country_id_d3five': fields.many2one('res.country', 'Country'),
		# Fields for Individual trustee 6
		'settlor_donord3six':fields.boolean('Settlor/Donor'),
		'protector_d3six':fields.boolean('Protector'),
		'beneficiary_d3six':fields.boolean('Beneficiary'),
		'name_d3six':fields.char('Name',select=True),
		'birth_death_d3six':fields.date('Date of Birth or Death'),
		'birth_d3six':fields.boolean('Birth'),
		'death_d3six':fields.boolean('Death'),
		'street_d3six': fields.char('Street', size=128),
        	'street2_d3six': fields.char('Street2', size=128),
        	'zip_d3six': fields.char('PostCode', change_default=True, size=24),
        	'city_d3six': fields.char('City', size=128),
        	'state_id_d3six': fields.many2one("res.country.state", 'State'),
       		'country_id_d3six': fields.many2one('res.country', 'Country'),
		'class_of_beneficiary':fields.text(''),
		#Fields for Corporate trustees
		'corporate_point_one':fields.boolean('Point one'),
		'corporate_point_two':fields.boolean('Point Two'),
		'corporate_point_three':fields.boolean('Point Three'),
		'corporate_point_four':fields.boolean('Point Four'),
		'corporate_point_five':fields.boolean('Point Five'),
		'corporate_point_six':fields.boolean('Point Six'),
		'corporate_point_seven':fields.boolean('Point seven'),
		'corporate_point_eight':fields.boolean('Point eight'),
		#Fields for Section E
		'parties_to_contract_sectione':fields.text(''),
		#Declaration of client 1
		'client_name_sectioneone':fields.char('Client name',select=True),
		'capacity_sectioneone':fields.char('Capacity'),
		'signature_sectioneone':fields.char('Signature of client'),
		'date_sectioneone':fields.date('Date'),
		#Declaration of client 2
		'client_name_sectionetwo':fields.char('Client name',select=True),
		'capacity_sectionetwo':fields.char('Capacity'),
		'signature_sectionetwo':fields.char('Signature of client'),
		'date_sectionetwo':fields.date('Date'),
		#Declaration of client 3
		'client_name_sectionethree':fields.char('Client name',select=True),
		'capacity_sectionethree':fields.char('Capacity'),
		'signature_sectionethree':fields.char('Signature of client'),
		'date_sectionethree':fields.date('Date'),
		#Declaration of client 4
		'client_name_sectionefour':fields.char('Client name',select=True),
		'capacity_sectionefour':fields.char('Capacity'),
		'signature_sectionefour':fields.char('Signature of client'),
		'date_sectionefour':fields.date('Date'),
		#Declaration by financial adviser
		'advisor_name_sectione':fields.char('Full name of financial adviser'),
		'advisor_sign_sectione':fields.char('Signature of financial adviser'),
		'introducer_name_sectione':fields.char('Full name of introducer firm'),
		'account_no_sectione':fields.char('Account number/CID number'),
		'date_sectione':fields.date('Date'),

		
        }
	_defaults = {
		'is_company':False,
		'is_joint':False,
		'user_id': lambda obj, cr, uid, context: uid,
		'name': lambda obj, cr, uid, context: '/',
		'state':'sectiona',
		'date_create':fields.date.context_today,
		'active':True,
		'income_from_employment':False,
		'income_from_your_business':False,
		'income_from_your_business_two':False,
		'unearned_income':False,
		'investment_saving':False,
		'maturing_investment':False,
		'sale_of_property':False,
		'sale_of_interest_company':False,
		'sale_of_shares':False,
		'inheritance':False,
		'loan':False,
		'gift':False,
		'compensation':False,
		'competition':False,
		'other':False,
		
	}
	_sql_constraints = [
		('name_uniq', 'unique(name_client, name_contract)', 'Name of the client must be unique per Contractor!'),
	]
	_description='Suisee Asset Management'
	_order = "name_client asc"
	


	def create(self, cr, uid, vals, context=None):
		if vals.get('name','/')== '/':
			vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'suisse.capital.client.form') or '/'
		clients_no =  super(suisse_capital_client_form, self).create(cr, uid, vals, context=context)
		return clients_no

	def change_state(self,cr,uid,ids,context=None):
		for i in self.browse(cr,uid,ids,context=context):
		    self.write(cr,uid,i.id,{'state':context['state']})
		return True
	
	def view_bank(self, cr, uid, ids, context=None):
		mod_obj = self.pool.get('ir.model.data')
		res = mod_obj.get_object_reference(cr, uid, 'suisse_asset_module', 'company_bank_account_form_view')
		print res
		res_id = res and res[1]
		return {
		    'name': _('Company Bank Account'),
		    'view_type': 'form',
		    'view_mode': 'form',
		    'view_id': [res_id],
		    'res_model': 'bank.account.opening.company',
		    'context': "{}",
		    'type': 'ir.actions.act_window',
		    'nodestroy': True,
		    'target': 'current',
		    
		}
	

suisse_capital_client_form()

class  suisse_capital_bank_account_multi(osv.osv):
	_columns = {
		'bank_name':fields.char('Bank Name',size=200),
		'account_no':fields.char('Account Number', change_default=True),
		'suisse_capital_bank':fields.many2one('suisse.capital.client.form','Client', select=True, ondelete='cascade'),
	}
	_defaults = {
		'account_no':38034033222,
	}
	
	_name = 'suisse.capital.bank.account.multi'
	_description = 'Suisse client bank account'

suisse_capital_bank_account_multi()
