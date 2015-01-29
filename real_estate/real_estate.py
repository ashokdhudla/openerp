from openerp.osv import osv,fields
import datetime
from datetime import date
from datetime import timedelta
import urllib

# rentals
class real_estate_view(osv.osv):
	_name = 'real.estate'
	_descrption = "This is object for real estate"

	# def serial(self,cr,uid,ids,field_name, arg, context=None):
	# 	res={}
	# 	counter=0
	# 	for i in self.browse(cr,uid,ids,context=None):
	# 		res[i.id]={
	# 				'real_ref':1
	# 			}
	# 		counter+=1
	# 		res[i.id]['real_ref'] = 'UH-R-100'+str(counter)
	# 	return res
	_columns = {
		# 'new_field': fields.char('New Field', size=16,readonly=True),
		# 'sl_no':fields.function(serial_inc,string='Sl.No',type="char",multi="sums" ,readonly=True),
		'listing_type' : fields.char('Listing Type',readonly=True),
		# 'listing_type' : fields.selection([('rentals', 'Rentals'),('sales', 'Sales')], 'Listing type',required=True),
		'real_ref' : fields.char('Ref',size=25,readonly=True),
		'unit_no' : fields.char('Unit No',size=50,required=True),
		'type' : fields.char('Type',size=50,required=False),
		'street_no' : fields.char('Street No',size=50,required=False),
		'floor' : fields.char('Floor',size=50,required=False),
		'category_name' : fields.selection([('apartment','Apartement'),('villa','Villa'),
											('office','Office'),('retail','Retail'),
											('hotel_apartment','Hotel Apartement'),
											('warehouse','Ware House'),('land_commercial','Land Commercial'),
											('labour_camp','Labour camp'),('res_build','Residential Building'),
											('mul_sale_units','Multiple Sale Units'),('land_res','Land Residential'),
											('com_ful_buil','Commercial Full Building'),('penthouse','Penthouse'),
											('duplex','Duplex'),('loft_aprt','Loft apartment'),
											('townhouse','Townhouse'),('hotel','Hotel'),
											('land_mix_use','Land Mix Use'),('comp','Compound')],'Category',required=True),
		# 'category_name' : fields.many2one('cat.name','Category'),
		'emirate' : fields.many2one('emirates.name','Emirate',required=True),
		'location' : fields.many2one('location.name','Location'),
		'sub_location' : fields.many2one('sublocation.name','Sub-Location'),
		# 'beds' : fields.char('Beds',size=50),
		# 'beds' : fields.many2one('beds.no','Beds'),
		'beds' : fields.selection([('studio','Studio'),('1_bed','1 bed'),('2_beds','2 beds'),
									('3_beds','3 beds'),('4_beds','4 beds'),('5_beds','5 beds'),
									('6_beds','6 beds'),('7_beds','7 beds'),('8_beds','8 beds'),
									('9_beds','9 beds'),('10_beds','10 beds'),('11_beds','11 beds'),
									('12_beds','12 beds')],'Beds'),
		'fitted' : fields.selection([('semi_fitted','Semi Fitted'),('fitted_space','Fitted Space'),
									('shel_core','Shell and Core')],'Fitted',invisible=True),
		# 'baths' : fields.many2one('baths.name','Baths'),
		'baths'  :  fields.selection([('1_bath','1 bath'),('2_baths','2 baths'),
									('3_baths','3 baths'),('4_baths','4 baths'),('5_baths','5 baths'),
									('6_baths','6 baths'),('7_baths','7 baths'),('8_baths','8 baths'),
									('9_baths','9 baths'),('10_baths','10 baths'),('11_baths','11 baths'),
									('12_baths','12 baths')],'Baths'),
		'bua' :  fields.float('BUA',required=True),
		'plot' :  fields.char('Plot'),
		'price' :fields.float('Price(AED)',required=True),
		'freq' : fields.selection([('freq','Frequency'),('p_day','Per Day'),('p_week','Per Week'),
									('p_month','Per Month'),('p_year','Per Year')],'Freq.'),
		'cheques' : fields.many2one('cheques.name','Cheques'),
		'parking' : fields.char('Parking'),
		'commission' : fields.float('Commission(%)',placeholer='%'),
		'commission_price' : fields.float('Commission(AED)',placeholer="Commission"),
		'deposit' :  fields.float('Deposit(%)',placeholer='%'),
		'deposit_price' : fields.float('Deposit(AED)',placeholer='Deposit'),
		'owner':fields.many2one('res.partner',"Owner",domain="[('customer','=',True)]",required=True),
		'listing_title' : fields.char('Listing Title',size=200,required=True),
		'desc' : fields.text('Description',size=268),
		'furnished' : fields.selection([('full','Furnished'),('p_fur','Partly Furnished'),('un_fur','Unfurnished')],'Furnished'),
		'view' : fields.char('View'),
		"image" : fields.binary("Pic1",help="Listing Image"),
		'img_id' : fields.one2many('add.img.rentals','mul_img'),
		'add_info_id' : fields.one2many('add.info','add_infor'),
		'portals' : fields.char('Portals'),
		'oth_med' :  fields.char('Other Media'),
		'featr' :  fields.char('Features'),
		'date_listed' : fields.datetime('Date Listed',readonly=True),
		'last_updated' : fields.datetime('Last Updated',readonly=True),
		'viewings' : fields.char('Viewings'),
		'leads' : fields.char('Leads'),
		'add_info' : fields.char('Additional Info'),
		'agent':fields.many2one('res.partner',"Agent",domain="[('customer','=',True)]"),
		'status' : fields.selection([('pub','Published'),('unpub','UnPublished')],'Status'),
		'managed' : fields.boolean('Managed'),
		'exec' : fields.boolean('Exclusive'),
		'invite' : fields.boolean('Invite'),
		# portal fields
		'dbzl' : fields.boolean('Dubizzle'),
		'just_rent' : fields.boolean('JustRentals'),
		'just_prop' : fields.boolean('JustProperty'),
		'prop_find' : fields.boolean('PropertyFinder'),
		'bayut' : fields.boolean('Bayut'),
		'gn_prop' : fields.boolean('GNproperty'),
		'zoopla' : fields.boolean('Zoopla'),
		'right_move' : fields.boolean('Rightmove'),
		'own_web' : fields.boolean('Own Website'),
		# add other media fields
		'youtube_vid_link' : fields.char('YouTube video link',email=True),
		'360_vir_link' : fields.char('360 Virtual tour link'),
		'aud_tour_link' : fields.char('Audio tour link'),
		'vid_tour_link' : fields.char('Video tour link'),
		'qr_code_link' : fields.char('Qr Code link'),
		'pdf_brou' : fields.binary('PDF brouchure'),
		'upload_video' : fields.binary('Upload vidoe'),
		# additional information fields
		'prop_sta' : fields.selection([('avil','Available'),('pend','Pending'),
										('sold_rented','Sold/Rented'),('upcmg','Upcoming'),
										('reser','Reserved')],'Property status'),
		'source_listing' : fields.selection([('not_specified','Not Specified'),('7days','7 days'),
										('agent','agent'),('al_ayam','Al Ayam'),
										('al_bayan','al_bayan'),('al_khaleej','Al Khaleej'),
										('al_rai','al_Rai'),('al_watan','Al Watan'),
										('arab_times','Arab Times'),('asharq_al_awsat','Asharq Al Awsat'),
										('bank_ref','Bank Referral'),('bayut_com','Bayut.com'),
										('cold_call','Cold call'),('colors_tv','Colors Tv'),
										('db','Database'),('direct_call','Direct call'),
										('Dubizzle_com','Dubizzle.com'),('direct_client','Direct Client'),
										('dzooom_com','Dzooom.com')],'Source of listing'),
		'featurd' : fields.selection([('yes','yes')],'Featured'),
		'dewa_no_ai' : fields.char('DEWA Number'),
		'str_ai': fields.char('STR#'),
		'next_avil_ai': fields.datetime('Next available'),
		'remind_ai': fields.selection([('never','Never'),('1day','1 day'),
										('1week','1week'),('2weeks','2 weeks'),
										('1month','1 month'),('2months','2 months'),
										('3months','3 months'),('4months','4 months'),('6months','6months')],'Remind'),
		'new_notes' : fields.text('New Notes'),
		'key_loc' : fields.char('Key Location'),
		'prop_tenate' : fields.boolean('Property Tenanted?'),
		'rent_at_ai' : fields.char('Rented at'),
		'rented_until' : fields.datetime('Rented Until'),
		'main_fee' : fields.char('Maintenance Fee'),
		'price/sqft' : fields.char('Price/sq ft'),
		'doc_name' : fields.char('Doc name',placeholer="Document Name"),
		'doc_file' : fields.binary('upload'),
		'doc_text' : fields.text('Doc text'),
		# features and amenties fields
		'balcony' : fields.boolean('Balcony'),
		'brdband_ready' : fields.boolean('Broandband ready'),
		'carpets' : fields.boolean('Carpets'),
		'cov_park' : fields.boolean('Covered parking'),
		'ful_furnish' : fields.boolean('Fully furnished'),
		'jacuzzi' : fields.boolean('Jacuzzi'),
		'marble_floors' : fields.boolean('Marble Floores'),
		'on_mid_flr' : fields.boolean('On mid floors'),
		'prt_grg' : fields.boolean('Private garage'),
		'prop_lndsc_grd' : fields.boolean('Professionally landscaped garden'),
		'sld_wd_flrs' : fields.boolean('Solid Wood Floors'),
		'upgrd_intr' : fields.boolean('Upgrade interior'),
		# 2nd column
		'bm_park' : fields.boolean('Basement parking'),
		'central_ac' : fields.boolean('Central air conditioning'),
		'drvs_ac' : fields.boolean('Drivers ac'),
		'gazebo_otdr_entng_area' : fields.boolean('Gazebo and outdoor Entertaining area'),
		'ktn_wht_gds' : fields.boolean('Kitchen white goods'),
		'on_hgh_flrs' : fields.boolean('On high floors'),
		'prt_fur' : fields.boolean('Part furnished'),
		'prvt_grdn' : fields.boolean('Private garden'), 
		'sauna' : fields.boolean('sauna'), 
		'stm_rm' : fields.boolean('Steam Room'), 
		'vw_grds' : fields.boolean('View of gardens'), 
		'bbq_area' : fields.boolean('BBQ area'),
		# 3rd column 
		'blt_wrdrobes' : fields.boolean('Built in wardrobes'),
		'cmnty_vw' : fields.boolean('Community View'), 
		'fl_ft_kchn' : fields.boolean('Full fitted kitchen'), 
		'gym' : fields.boolean('Gynasium'), 
		'mds_rm' : fields.boolean("Maid's room"), 
		'on_lw_flr' : fields.boolean('On low floor'), 
		'pts_awd' : fields.boolean('Pets allowed'), 
		'prvt_smng_pl' : fields.boolean('Private swimming pool'), 
		'shrd_smng_pl' : fields.boolean('Shared swimming pool'),
		'stdy' : fields.boolean('Study'),
		'vw_sea_wtr' : fields.boolean('View of sea/water'),
		#4th column
		'chndrn_nrsy' : fields.boolean('Chindrens nursary'),
		'glf_clb_hse' : fields.boolean('Golf club and clubhouse'),
		'polo_clb_hse' : fields.boolean('Polo club and clubhouse'), 
		'pub_trpt' : fields.boolean('Public transport'),
		'shps' : fields.boolean('Shops'),
		#5th column
		'chdrn_ply_ara' : fields.boolean("Chindren's play area"),
		'mtr_stn' : fields.boolean('Metro station'),
		'pub_prk' : fields.boolean('Public park'),
		'restrnt' : fields.boolean('Restaurents'),
		'squash_crt' : fields.boolean('Squash courts'),
		#6th column
		'cmnl_grd' : fields.boolean('Communal gardens'),
		'msue' : fields.boolean('Mosque'),
		'pub_prkng' : fields.boolean('Public parking'),
		'shpg_mall' : fields.boolean('Shopping mall'),
		'tens_crt' : fields.boolean('Tennis court'),
		# Area information
		'schls_ari' : fields.char('Schools'),
		'metrs_ari' : fields.char('Metros'),
		'shpg_ml_ari' : fields.char('Shopping Malls'),
		'msqs_ari' : fields.char('Mosques'),
		'bechs_ari' : fields.char('Beaches'),
		'spr_mrts_ari' : fields.char('Super Markets'),
		'park_ari' : fields.char('Park'),
		#maps fields
		'longitude':fields.char('Longitude'),
		'latitude':fields.char('Latitude'),

	}
	_defaults = {
				'freq' : 'p_year',
				'listing_type' : 'Rentals',
				'real_ref': lambda self,cr,uid,context={}: self.pool.get('ir.sequence').get(cr, uid, 'sequence_code'),
				'dbzl' : True,
				'just_rent' :  True,
				'just_prop' :  True,
				'prop_find' :  True,
				'bayut' :  True,
				'gn_prop' :  True,
				'zoopla' :  True,
				'right_move' :  True,
				'own_web' :  True,
				'date_listed' : fields.datetime.now,
				'last_updated' : fields.datetime.now,
				}
	_rec_name='real_ref'


	def _check_length(self, cr, uid, ids, context=None):
		record = self.browse(cr, uid, ids, context=context)
		print "helooooooo"
		for data in record:
			if data.commission < 0:
				return False
		return True
	_constraints = [(_check_length, 'Error: Length must be Positive', ['commission'])]

	def write(self,cr,uid,ids,vals,context=None):
		today = datetime.datetime.now()
		vals.update({'last_updated' : today })
		print "valssssssssssss",vals
		# return True

		return super(real_estate_view, self).write(cr, uid, ids, vals, context=context)
	
	def onchange_price_discount(self,cr,uid,ids,price,commission,commission_price,deposit,deposit_price,context=None):
		print "onchange_price_discount is calling"
		res = {}
		if price:
			com_price = (price/100)*commission
			deposit_price = (price/100)*deposit
			res.update({'commission_price':float(com_price),'deposit_price':float(deposit_price)})
		return {'value':res}

	def open_map(self, cr, uid, ids, context=None):
		address_obj= self.pool.get('atm.info')
		partner = address_obj.browse(cr, uid, ids, context=context)[0]
		url="http://maps.google.com/maps?oi=map&q="
		if partner.longitude:
			url+=partner.longitude.replace(' ','+')
		if partner.latitude:
			url+= ',' + partner.latitude.replace(' ','+')
		return {
			'type': 'ir.actions.act_url','url':url,'target': 'new'}

	def geo_localize(self, cr, uid, ids, context=None):

		partner = self.browse(cr,uid,ids)
		latitude = partner[0].latitude
		longitude = partner[0].longitude
		geo = {}
		if latitude or longitude:
			geo['lat'] = latitude
			geo['lng'] = longitude
			return float(geo['lat']), float(geo['lng'])
		return True
real_estate_view()
class category_name(osv.osv):
	_name = 'cat.name'
	_columns = {
		'cat_name' :fields.char('Name',required=True),
	}
	_rec_name = 'cat_name'
category_name()

class emirate_name(osv.osv):
	_name = 'emirates.name'
	_columns = {
		'emi_name':fields.char('Emirate Name',required=True),
	}
	_rec_name = 'emi_name'
emirate_name()

class location_name(osv.osv):
	_name = 'location.name'
	_columns = {
		'loc_name' :fields.char('Location Name',required=True),
	}
	_rec_name = 'loc_name'
location_name()

class sublocation_name(osv.osv):
	_name = 'sublocation.name'
	_columns = {
		'subloc_name' :fields.char('Sub-Location Name',required=True),
		'buld_name' : fields.char('Building Name'),
	}
	_rec_name = 'subloc_name'
sublocation_name()

class bed_no(osv.osv):
	_name = 'beds.no'
	_columns = {
		'beds' :fields.char('Beds',required=True,placeholer="2 beds"),
	}
	_rec_name = 'beds'
bed_no()

class bath_name(osv.osv):
	_name = 'baths.name'
	_columns = {
		'bath_name' :fields.char('Baths',required=True,placeholer="2 baths"),
	}
	_rec_name = 'bath_name'
bath_name()
class cheque_name(osv.osv):
	_name = 'cheques.name'
	_columns = {
		'cheque_name' :fields.char('Cheque Name',required=True,placeholer="1 Cheque"),
	}
	_rec_name = 'cheque_name'
cheque_name()

class mul_img_rentals(osv.osv):
	_name = 'add.img.rentals'
	def serial_inc(self,cr,uid,ids,field_name, arg, context=None):
		res={}
		counter=0
		for i in self.browse(cr,uid,ids,context=None):
			res[i.id]={
					'sl_no':1
				}
			counter+=1
			res[i.id]['sl_no'] = counter
		return res
	_columns = {
			'mul_img' : fields.many2one('real.estate'),
			'sl_no':fields.function(serial_inc,string='Sl.No',type="char",multi="sums" ,readonly=True),
			"image" : fields.binary("Image",help="Listing Image"),
	}
	def _check_length(self, cr, uid, ids, context=None):
		record = self.browse(cr, uid, ids, context=context)
		print "check"
		for data in record:
			img_ids = self.pool.get('add.img.rentals').search(cr,uid,[('mul_img','=',data.mul_img.id)])
			if len(img_ids) > 4:
				return False
		return True
	_constraints = [(_check_length, 'Error: we can not create images more than 4', ['sl_no'])]


mul_img_rentals()

class add_info(osv.osv):
	_name = 'add.info'
	# def serial_inc_info(self,cr,uid,ids,field_name, arg, context=None):
	# 	res={}
	# 	counter=0
	# 	for i in self.browse(cr,uid,ids,context=None):
	# 		res[i.id]={
	# 				'sl_no':1
	# 			}
	# 		counter+=1
	# 		res[i.id]['sl_no'] = counter
	# 	return res
	_columns = {
			'add_infor' : fields.many2one('real.estate'),
			# 'sl_no':fields.function(serial_inc_info,string='Sl.No',type="char",multi="sums" ,readonly=True),
			# "pror_status" : fields.selection([('avail','Available'),('pend','Pending'),('sold_rental','Sold/Rental'),
			# 						('upcmng','Upcomming'),('reserved','Reserved')],'Property Status'),
			# "sourc_listing" : fields.selection([('not_specified','Not Specified'),('7days','7 days'),('agent','Agent'),
			# 						('al_ayam','Al Ayam'),('al_rai','Al Rai')],'Source of listing'),
			'dewa_no' : fields.integer('DEWA Number'),
	}
add_info()

# sales 
class real_estate_sales_view(osv.osv):
	_name = 'real.estate.sales'
	_descrption = "This is object for real estate sales "
	_columns = {
		'listing_type' : fields.char('Listing Type',readonly=True),
		'real_ref_sales' : fields.char('Ref',size=25,readonly=True),
		'unit_no' : fields.char('Unit No',size=50,required=True),
		'type' : fields.char('Type',size=50,required=False),
		'street_no' : fields.char('Street No',size=50,required=False),
		'floor' : fields.char('Floor',size=50,required=False),
		'category_name' : fields.selection([('apartment','Apartement'),('villa','Villa'),
											('office','Office'),('retail','Retail'),
											('hotel_apartment','Hotel Apartement'),
											('warehouse','Ware House'),('land_commercial','Land Commercial'),
											('labour_camp','Labour camp'),('res_build','Residential Building'),
											('mul_sale_units','Multiple Sale Units'),('land_res','Land Residential'),
											('com_ful_buil','Commercial Full Building'),('penthouse','Penthouse'),
											('duplex','Duplex'),('loft_aprt','Loft apartment'),
											('townhouse','Townhouse'),('hotel','Hotel'),
											('land_mix_use','Land Mix Use'),('comp','Compound')],'Category',required=True),
		'emirate' : fields.many2one('emirates.name','Emirate',required=True),
		'location' : fields.many2one('location.name','Location'),
		'sub_location' : fields.many2one('sublocation.name','Sub-Location'),
		'beds' : fields.selection([('studio','Studio'),('1_bed','1 bed'),('2_beds','2 beds'),
									('3_beds','3 beds'),('4_beds','4 beds'),('5_beds','5 beds'),
									('6_beds','6 beds'),('7_beds','7 beds'),('8_beds','8 beds'),
									('9_beds','9 beds'),('10_beds','10 beds'),('11_beds','11 beds'),
									('12_beds','12 beds')],'Beds'),
		'fitted' : fields.selection([('semi_fitted','Semi Fitted'),('fitted_space','Fitted Space'),
									('shel_core','Shell and Core')],'Fitted',invisible=True),
		'baths'  :  fields.selection([('1_bath','1 bath'),('2_baths','2 baths'),
									('3_baths','3 baths'),('4_baths','4 baths'),('5_baths','5 baths'),
									('6_baths','6 baths'),('7_baths','7 baths'),('8_baths','8 baths'),
									('9_baths','9 baths'),('10_baths','10 baths'),('11_baths','11 baths'),
									('12_baths','12 baths')],'Baths'),
		'bua' :  fields.float('BUA',required=True),
		'plot' :  fields.char('Plot'),
		'price' :fields.float('Price(AED)',required=True),
		'freq' : fields.selection([('freq','Frequency'),('p_day','Per Day'),('p_week','Per Week'),
									('p_month','Per Month'),('p_year','Per Year')],'Freq.'),
		'show_poa' : fields.boolean('Show POA'),
		'price_sqft' : fields.float('Price / sq ft'),
		'parking' : fields.char('Parking'),
		'commission' : fields.float('Commission(%)',placeholer='%'),
		'commission_price' : fields.float('Commission(AED)',placeholer="Commission"),
		'deposit' :  fields.float('Deposit(%)',placeholer='%'),
		'deposit_price' : fields.float('Deposit(AED)',placeholer='Deposit'),
		'owner':fields.many2one('res.partner',"Owner",domain="[('customer','=',True)]",required=True),
		'listing_title' : fields.char('Listing Title',size=200,required=True),
		'desc' : fields.text('Description',size=268),
		'furnished' : fields.selection([('full','Furnished'),('p_fur','Partly Furnished'),('un_fur','Unfurnished')],'Furnished'),
		'view' : fields.char('View'),
		"image" : fields.binary("Pic1",help="Listing Image"),
		'img_id' : fields.one2many('add.img','mul_img'),
		'add_info_id' : fields.one2many('add.info','add_infor'),
		'date_listed' : fields.datetime('Date Listed',readonly=True),
		'last_updated' : fields.datetime('Last Updated',readonly=True),
		'viewings' : fields.char('Viewings'),
		'leads' : fields.char('Leads'),
		'add_info' : fields.char('Additional Info'),
		'agent':fields.many2one('res.partner',"Agent",domain="[('customer','=',True)]"),
		'status' : fields.selection([('pub','Published'),('unpub','UnPublished')],'Status'),
		'managed' : fields.boolean('Managed'),
		'exec' : fields.boolean('Exclusive'),
		'invite' : fields.boolean('Invite'),
		# portal fields
		'dbzl' : fields.boolean('Dubizzle'),
		'just_rent' : fields.boolean('JustRentals'),
		'just_prop' : fields.boolean('JustProperty'),
		'prop_find' : fields.boolean('PropertyFinder'),
		'bayut' : fields.boolean('Bayut'),
		'gn_prop' : fields.boolean('GNproperty'),
		'zoopla' : fields.boolean('Zoopla'),
		'right_move' : fields.boolean('Rightmove'),
		'own_web' : fields.boolean('Own Website'),
		# add other media fields
		'youtube_vid_link' : fields.char('YouTube video Link',email=True),
		'360_vir_link' : fields.char('360 Virtual tour link'),
		'aud_tour_link' : fields.char('Audio tour link'),
		'vid_tour_link' : fields.char('Video tour link'),
		'qr_code_link' : fields.char('Qr Code link'),
		'pdf_brou' : fields.binary('PDF broucher'),
		'upload_video' : fields.binary('Upload vidoe'),
		# additional information fields
		'prop_sta' : fields.selection([('avil','Available'),('pend','Pending'),
										('sold_rented','Sold/Rented'),('upcmg','Upcoming'),
										('reser','Reserved')],'Property status'),
		'source_listing' : fields.selection([('not_specified','Not Specified'),('7days','7 days'),
										('agent','agent'),('al_ayam','Al Ayam'),
										('al_bayan','al_bayan'),('al_khaleej','Al Khaleej'),
										('al_rai','al_Rai'),('al_watan','Al Watan'),
										('arab_times','Arab Times'),('asharq_al_awsat','Asharq Al Awsat'),
										('bank_ref','Bank Referral'),('bayut_com','Bayut.com'),
										('cold_call','Cold call'),('colors_tv','Colors Tv'),
										('db','Database'),('direct_call','Direct call'),
										('Dubizzle_com','Dubizzle.com'),('direct_client','Direct Client'),
										('dzooom_com','Dzooom.com')],'Source of listing'),
		'featurd' : fields.selection([('yes','yes')],'Featured'),
		'dewa_no_ai' : fields.char('DEWA Number'),
		'str_ai': fields.char('STR#'),
		'next_avil_ai': fields.datetime('Next available'),
		'remind_ai': fields.selection([('never','Never'),('1day','1 day'),
										('1week','1week'),('2weeks','2 weeks'),
										('1month','1 month'),('2months','2 months'),
										('3months','3 months'),('4months','4 months'),('6months','6months')],'Remind'),
		'new_notes' : fields.text('New Notes'),
		'key_loc' : fields.char('Key Location'),
		'prop_tenate' : fields.boolean('Property Tenanted?'),
		'rent_at_ai' : fields.char('Rented at'),
		'rented_until' : fields.datetime('Rented Until'),
		'main_fee' : fields.char('Maintenance Fee'),
		'price/sqft' : fields.char('Price/sq ft'),
		'doc_name' : fields.char('Doc name',placeholer="Document Name"),
		'doc_file' : fields.binary('upload'),
		'doc_text' : fields.text('Doc text'),
		# features and amenties fields
		'balcony' : fields.boolean('Balcony'),
		'brdband_ready' : fields.boolean('Broandband ready'),
		'carpets' : fields.boolean('Carpets'),
		'cov_park' : fields.boolean('Covered parking'),
		'ful_furnish' : fields.boolean('Fully furnished'),
		'jacuzzi' : fields.boolean('Jacuzzi'),
		'marble_floors' : fields.boolean('Marble Floores'),
		'on_mid_flr' : fields.boolean('On mid floors'),
		'prt_grg' : fields.boolean('Private garage'),
		'prop_lndsc_grd' : fields.boolean('Professionally landscaped garden'),
		'sld_wd_flrs' : fields.boolean('Solid Wood Floors'),
		'upgrd_intr' : fields.boolean('Upgrade interior'),
		# 2nd column
		'bm_park' : fields.boolean('Basement parking'),
		'central_ac' : fields.boolean('Central air conditioning'),
		'drvs_ac' : fields.boolean('Drivers ac'),
		'gazebo_otdr_entng_area' : fields.boolean('Gazebo and outdoor Entertaining area'),
		'ktn_wht_gds' : fields.boolean('Kitchen white goods'),
		'on_hgh_flrs' : fields.boolean('On high floors'),
		'prt_fur' : fields.boolean('Part furnished'),
		'prvt_grdn' : fields.boolean('Private garden'), 
		'sauna' : fields.boolean('sauna'), 
		'stm_rm' : fields.boolean('Steam Room'), 
		'vw_grds' : fields.boolean('View of gardens'), 
		'bbq_area' : fields.boolean('BBQ area'),
		# 3rd column 
		'blt_wrdrobes' : fields.boolean('Built in wardrobes'),
		'cmnty_vw' : fields.boolean('Community View'), 
		'fl_ft_kchn' : fields.boolean('Full fitted kitchen'), 
		'gym' : fields.boolean('Gynasium'), 
		'mds_rm' : fields.boolean("Maid's room"), 
		'on_lw_flr' : fields.boolean('On low floor'), 
		'pts_awd' : fields.boolean('Pets allowed'), 
		'prvt_smng_pl' : fields.boolean('Private swimming pool'), 
		'shrd_smng_pl' : fields.boolean('Shared swimming pool'),
		'stdy' : fields.boolean('Study'),
		'vw_sea_wtr' : fields.boolean('View of sea/water'),
		#4th column
		'chndrn_nrsy' : fields.boolean('Chindrens nursary'),
		'glf_clb_hse' : fields.boolean('Golf club and clubhouse'),
		'polo_clb_hse' : fields.boolean('Polo club and clubhouse'), 
		'pub_trpt' : fields.boolean('Public transport'),
		'shps' : fields.boolean('Shops'),
		#5th column
		'chdrn_ply_ara' : fields.boolean("Chindren's play area"),
		'mtr_stn' : fields.boolean('Metro station'),
		'pub_prk' : fields.boolean('Public park'),
		'restrnt' : fields.boolean('Restaurents'),
		'squash_crt' : fields.boolean('Squash courts'),
		#6th column
		'cmnl_grd' : fields.boolean('Communal gardens'),
		'msue' : fields.boolean('Mosque'),
		'pub_prkng' : fields.boolean('Public parking'),
		'shpg_mall' : fields.boolean('Shopping mall'),
		'tens_crt' : fields.boolean('Tennis court'),
		# Area information
		'schls_ari' : fields.char('Schools'),
		'metrs_ari' : fields.char('Metros'),
		'shpg_ml_ari' : fields.char('Shopping Malls'),
		'msqs_ari' : fields.char('Mosques'),
		'bechs_ari' : fields.char('Beaches'),
		'spr_mrts_ari' : fields.char('Super Markets'),
		'park_ari' : fields.char('Park'),
		#map for sales
		'longitude':fields.char('Longitude'),
		'latitude':fields.char('Latitude'),
	}
	_defaults = {
				'freq' : 'p_year',
				'listing_type' : 'Sales',
				'real_ref_sales': lambda self,cr,uid,context={}: self.pool.get('ir.sequence').get(cr, uid, 'sequence_ref_sales'),
				'dbzl' : True,
				'just_rent' :  True,
				'just_prop' :  True,
				'prop_find' :  True,
				'bayut' :  True,
				'gn_prop' :  True,
				'zoopla' :  True,
				'right_move' :  True,
				'own_web' :  True,
				'date_listed' : fields.datetime.now,
				'last_updated' : fields.datetime.now,
				}
	_rec_name='real_ref_sales'

	# def _check_limit_img(self,cr,uid,ids,vals,context=None):
	# 	# self_obj = self.browse(cr, uid, ids, context=context); 
	# 	# lenth = len(self_obj.orderline)
	# 	print "idsss length",len(ids)
	# 	return False

	# _constraints = [
	# 	(_check_limit_img, 'Error ! You cannot create more than 5 images.', ['img_id'])
	# ]

	def write(self,cr,uid,ids,vals,context=None):
		today = datetime.datetime.now()
		vals.update({'last_updated' : today })
		return super(real_estate_sales_view, self).write(cr, uid, ids, vals, context=context)				

	
	def onchange_price_discount(self,cr,uid,ids,price,commission,commission_price,deposit,deposit_price,bua,context=None):
		print "onchange_price_discount is calling"
		res = {}
		if price:
			com_price = (price/100)*commission
			deposit_price = (price/100)*deposit
			if bua:
				sq_price = price/bua
				res.update({'price_sqft':sq_price})
			res.update({'commission_price':float(com_price),'deposit_price':float(deposit_price)})
		return {'value':res}

	def open_map(self, cr, uid, ids, context=None):
		address_obj= self.pool.get('atm.info')
		partner = address_obj.browse(cr, uid, ids, context=context)[0]
		url="http://maps.google.com/maps?oi=map&q="
		if partner.longitude:
			url+=partner.longitude.replace(' ','+')
		if partner.latitude:
			url+= ',' + partner.latitude.replace(' ','+')
		return {
			'type': 'ir.actions.act_url','url':url,'target': 'new'}

	def geo_localize(self, cr, uid, ids, context=None):

		partner = self.browse(cr,uid,ids)
		latitude = partner[0].latitude
		longitude = partner[0].longitude
		geo = {}
		if latitude or longitude:
			geo['lat'] = latitude
			geo['lng'] = longitude
			return float(geo['lat']), float(geo['lng'])
		return True
real_estate_sales_view()
class category_name(osv.osv):
	_name = 'cat.name'
	_columns = {
		'cat_name' :fields.char('Name',required=True),
	}
	_rec_name = 'cat_name'
category_name()

class emirate_name(osv.osv):
	_name = 'emirates.name'
	_columns = {
		'emi_name':fields.char('Emirate Name',required=True),
	}
	_rec_name = 'emi_name'
emirate_name()

class location_name(osv.osv):
	_name = 'location.name'
	_columns = {
		'loc_name' :fields.char('Location Name',required=True),
	}
	_rec_name = 'loc_name'
location_name()

class location_name(osv.osv):
	_name = 'sublocation.name'
	_columns = {
		'subloc_name' :fields.char('Sub-Location Name',required=True),
	}
	_rec_name = 'subloc_name'
location_name()

class bed_no(osv.osv):
	_name = 'beds.no'
	_columns = {
		'beds' :fields.char('Beds',required=True,placeholer="2 beds"),
	}
	_rec_name = 'beds'
bed_no()

class bath_name(osv.osv):
	_name = 'baths.name'
	_columns = {
		'bath_name' :fields.char('Baths',required=True,placeholer="2 baths"),
	}
	_rec_name = 'bath_name'
bath_name()
class cheque_name(osv.osv):
	_name = 'cheques.name'
	_columns = {
		'cheque_name' :fields.char('Cheque Name',required=True,placeholer="1 Cheque"),
	}
	_rec_name = 'cheque_name'
cheque_name()

class mul_img(osv.osv):
	_name = 'add.img'
	def serial_inc(self,cr,uid,ids,field_name, arg, context=None):
		res={}
		counter=0
		for i in self.browse(cr,uid,ids,context=None):
			res[i.id]={
					'sl_no':1
				}
			counter+=1
			res[i.id]['sl_no'] = counter
		return res
	_columns = {
			'mul_img' : fields.many2one('real.estate'),
			'sl_no':fields.function(serial_inc,string='Sl.No',type="char",multi="sums" ,readonly=True),
			"image" : fields.binary("Image",help="Listing Image"),
	}

	def _check_length(self, cr, uid, ids, context=None):
		record = self.browse(cr, uid, ids, context=context)
		print "check"
		for data in record:
			img_ids = self.pool.get('add.img').search(cr,uid,[('mul_img','=',data.mul_img.id)])
			if len(img_ids) > 4:
				return False
		return True
	_constraints = [(_check_length, 'Error: we can not create images more than 4', ['sl_no'])]
mul_img()

class add_info(osv.osv):
	_name = 'add.info'
	# def serial_inc_info(self,cr,uid,ids,field_name, arg, context=None):
	# 	res={}
	# 	counter=0
	# 	for i in self.browse(cr,uid,ids,context=None):
	# 		res[i.id]={
	# 				'sl_no':1
	# 			}
	# 		counter+=1
	# 		res[i.id]['sl_no'] = counter
	# 	return res
	_columns = {
			'add_infor' : fields.many2one('real.estate'),
			# 'sl_no':fields.function(serial_inc_info,string='Sl.No',type="char",multi="sums" ,readonly=True),
			# "pror_status" : fields.selection([('avail','Available'),('pend','Pending'),('sold_rental','Sold/Rental'),
			# 						('upcmng','Upcomming'),('reserved','Reserved')],'Property Status'),
			# "sourc_listing" : fields.selection([('not_specified','Not Specified'),('7days','7 days'),('agent','Agent'),
			# 						('al_ayam','Al Ayam'),('al_rai','Al Rai')],'Source of listing'),
			'dewa_no' : fields.integer('DEWA Number'),
	}
add_info()




