from openerp.osv import osv,fields
from openerp.tools.translate import _

class stamp_merchant(osv.osv):
	_name="stamp.merchant"
	_description = "Stamp Merchant"
	# _inherit = ['mail.thread']
	_columns = {
		"name_organization" : fields.char('Name Of Organization',size=50,required=True,translate=True),
		"org_description" : fields.text('Organization Description'),
		"category_details" : fields.many2one('category.info','Category',required=True),
		"sub_category" : fields.char('Sub Category:(Cuisine : Italian,Bar)',size=50,required=True,translate=True),
		"address" : fields.text('Address(Head Office or Store)',required=True),
		"locality" : fields.many2one('locality.info','Locality',required=True),
		"email_id1" : fields.char('Email Id1',size=50,required=True),
		"email_id2" : fields.char('Email Id2',size=50,requird=False),
		"phone_no" : fields.char('Phone',size=50,required=True),
		"mobile_no" : fields.char('Mobile',size=50,requird=False),
		"point_contact_name" : fields.char('Point of Contact Name',size=50,required=True),
		"store_address" : fields.text('Address',required=True),
		'store_phone' : fields.char('Contact No',required=True),
		'store_emailid' : fields.char('Email Id',required=True),
		'total_table_count' : fields.integer('Total Table Count'),
		'preferred_language' : fields.char("Preferred Language for Staff Pamplets"),
		'offer_id' : fields.one2many('offer.info','offer_data'),
		'current_offer_id' : fields.one2many('current.offers','current_offers'),
		'offer_bday_anniversary' : fields.one2many('offers.bday','birthday_offers'),
		'promocode_offer_id' : fields.one2many('promocode.offers','promo_offers'),
		'lead_mngnt_desc' : fields.text("If Yes fill Details"),
		'lead_mngnt' : fields.selection([
			('yes','Yes'),
			('no','No'),
			],'Do you have an existing Lead management system?'),
		'silver_card' : fields.integer('Silver Card Privileges'),
		'gold_card' : fields.integer('Gold Card Privileges'),
		'platinum_card' : fields.integer('Platinum Card Privileges'),
		"upload" : fields.binary("upload file"),
	}
stamp_merchant()

class category_details(osv.osv):
	_name = 'category.info'
	_description = "Category information"
	_rec_name = 'category_name'
	_columns= {
		'category_id' : fields.char('Category Id',size=50),
		'category_name' : fields.char('Category Name',size=50,required=True),
	}
category_details()

class Locality_details(osv.osv):
	_name = 'locality.info'
	_description = "Locality information"
	_rec_name = 'locality_name'
	_columns= {
		'locality_code' : fields.char('Locality Code',size=50),
		'locality_name' : fields.char('Locality Name',size=50,required=True),
	}
Locality_details()

class offer_details(osv.osv):
	_name = 'offer.info'
	_description = "Offers information"
	_columns= {
		'offer_data' : fields.many2one('stamp.merchant'),
		'reward_name' : fields.char('Reward Name',size=50,required=True),
		'desc_reward' : fields.text('Reward Description'),
		'savings' : fields.integer('Savings',size=50,required=False),
		'stamp_no' : fields.char('Stamp No',required=True),
	}
offer_details()

class current_offer_details(osv.osv):
	_name = 'current.offers'
	_description = "Current Offers information"
	_columns= {
		'current_offers' : fields.many2one('stamp.merchant'),
		'current_reward_name' : fields.char('Reward Name',size=50,required=True),
		'desc_reward' : fields.text('Reward Description'),
		'stamp_no' : fields.char('Stamp No',required=True),
	}
current_offer_details()

class offers_birthday(osv.osv):
	_name = 'offers.bday'
	_description = "BirthDay/Aniversary Offers information"
	_columns = {
		'birthday_offers' : fields.many2one('stamp.merchant'),
		'birthday_reward_name' : fields.char('Reward Name',required=True),
		'birthday_reward_description' : fields.text('Rewards Description'),
		'birth_day_stamp_no' : fields.char('Stamp No',required=True),

	}
offers_birthday()

class promo_offer_details(osv.osv):
	_name = 'promocode.offers'
	_description = "promocode Offers information"
	_columns= {
		'promo_offers' : fields.many2one('stamp.merchant'),
		'promo_reward_name' : fields.char('Reward Name',size=50,required=True),
		'promo_desc_reward' : fields.text('Reward Description'),
		'stamp_no' : fields.char('Stamp No',required=True),
	}
promo_offer_details()
