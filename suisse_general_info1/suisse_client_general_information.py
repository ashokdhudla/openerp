from openerp.osv import fields, osv
from openerp import  tools
from openerp.tools.translate import _
import hashlib
import re
import logging
import os
import glob
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
class suisse_client_general_information(osv.osv):
	_name='suisse.client.general.info'
	_description='Client General Information'

	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
		for obj in self.browse(cr, uid, ids, context=context):
		    result[obj.id] = tools.image_get_resized_images(obj.image)
		return result
	def _set_image(self, cr, uid, id, name, value, args, context=None):
        	return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)

	def _has_image(self, cr, uid, ids, name, args, context=None):
		result = {}
		for obj in self.browse(cr, uid, ids, context=context):
		    result[obj.id] = obj.image != False
		return result
	_columns = {
		#Personal Details
		 'name':fields.char('CIN Number',select=True,required=True,readonly=True),
		 'image': fields.binary("Image",
		    help="This field holds the image used as avatar for this contact, limited to 1024x1024px"),
		'image_medium': fields.function(_get_image, fnct_inv=_set_image,
		    string="Medium-sized image", type="binary", multi="_get_image",
		    store={
		        'suisse.client.general.info': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
		    },
		    help="Medium-sized image of this contact. It is automatically "\
		         "resized as a 128x128px image, with aspect ratio preserved. "\
		         "Use this field in form views or some kanban views."),	
		'image_small': fields.function(_get_image, fnct_inv=_set_image,
            		string="Small-sized image", type="binary", multi="_get_image",
            		store={
                	'suisse.client.general.info': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
           		 },
           		 help="Small-sized image of this contact. It is automatically "\
                	 "resized as a 64x64px image, with aspect ratio preserved. "\
                 	"Use this field anywhere a small image is required."),
        	'has_image': fields.function(_has_image, type="boolean"),
		'is_company':fields.boolean('Is Company'),
		'is_joint':fields.boolean('Is Joint'),
		'user_id': fields.many2one('res.users', 'Created by', select=True, track_visibility='onchange'),
		'name_of_client_one':fields.char('Name',select=True),
		'name_of_client_two':fields.char('Name1',select=True),
		##Client 1
		'mobile': fields.char('Mobile', size=64,select=True),
		'nationality': fields.many2one('res.country', 'Nationality'),
		'resident_status': fields.selection([('nonres','Non-Resident'),('resident','Resident')],'Residential status'),
		'date_of_birth': fields.date('Date of Birth'),
		'sex':fields.selection([('male','Male'),('female','Female')],'Sex'),
		'marital_status':fields.selection([('single','Single'),('married','Married'),('divorced','Divorced'),('separated','Separated'),('widowed','Widowed')],'Marital Status'),
		'date_of_relationship':fields.date('Date of Relationship',select=1),
		'passport_number':fields.char('Passport Number',select=True),
		'pass_validity':fields.date('Passport Validity'),
		'visa_expiry':fields.date('Visa Expiry'),
		'relationship_manager':fields.many2one('suisse.relationship.manager','Relationship Manager'),
		'street_correspond': fields.char('Street', size=128),
        	'street2_correspond': fields.char('Street2', size=128),
        	'zip_correspond': fields.char('Postcode', change_default=True, size=24),
        	'city_correspond': fields.char('City', size=128),
        	'state_id_correspond': fields.many2one("res.country.state", 'State'),
        	'country_id_correspond': fields.many2one('res.country', 'Country'),
        	'country_correspond': fields.related('country_id', type='many2one', relation='res.country', string='Country',
                                  deprecated="This field will be removed as of OpenERP 7.1, use country_id instead"),
		'profession':fields.selection([('salaried','Salaried'),('self-employed','Self Employed'),('retired','Retired'),('homemaker','Home Maker')],'Business'),
		'designation':fields.char('Designation',select=1),
		'company_name':fields.char('Company name',select=1),
		'street_registration': fields.char('Street', size=128),
        	'street2_registration': fields.char('Street2', size=128),
        	'zip_registration': fields.char('Postcode', change_default=True, size=24),
        	'city_registration': fields.char('City', size=128),
        	'state_id_registration': fields.many2one("res.country.state", 'State'),
        	'country_id_registration': fields.many2one('res.country', 'Country'),
        	'country_registration': fields.related('country_id', type='many2one', relation='res.country', string='Country',
                                  deprecated="This field will be removed as of OpenERP 7.1, use country_id instead"),
		'telephone_one':fields.char('Telephone'),
		'fax_one':fields.char('Fax'),
		'street_business': fields.char('Street', size=128),
        	'street2_business': fields.char('Street2', size=128),
        	'zip_business': fields.char('Postcode', change_default=True, size=24),
        	'city_business': fields.char('City', size=128),
        	'state_id_business': fields.many2one("res.country.state", 'State'),
        	'country_id_business': fields.many2one('res.country', 'Country'),
        	'country_rbusiness': fields.related('country_id', type='many2one', relation='res.country', string='Country',
                                  deprecated="This field will be removed as of OpenERP 7.1, use country_id instead"),
		'telephone_two':fields.char('Telephone'),
		'fax_two':fields.char('Fax'),
		'email': fields.char('Email Id', size=240),
		##Client 2
		'mobile_client2': fields.char('Mobile', size=64,select=True),
		'nationality_client2': fields.many2one('res.country', 'Nationality'),
		'resident_status_client2': fields.selection([('nonres','Non-Resident'),('resident','Resident')],'Residential status'),
		'date_of_birth_client2': fields.date('Date of Birth'),
		'sex_client2':fields.selection([('male','Male'),('female','Female')],'Sex'),
		'marital_status_client2':fields.selection([('single','Single'),('married','Married'),('divorced','Divorced'),('separated','Separated'),('widowed','Widowed')],'Marital Status'),
		'date_of_relationship_client2':fields.date('Date of Relationship',select=1),
		'passport_number_client2':fields.char('Passport Number',select=True),
		'pass_validity_client2':fields.date('Passport Validity'),
		'visa_expiry_client2':fields.date('Visa Expiry'),
		'relationship_manager_client2':fields.many2one('suisse.relationship.manager','Relationship Manager'),
		'street_correspond_client2': fields.char('Street', size=128),
        	'street2_correspond_client2': fields.char('Street2', size=128),
        	'zip_correspond_client2': fields.char('Postcode', change_default=True, size=24),
        	'city_correspond_client2': fields.char('City', size=128),
        	'state_id_correspond_client2': fields.many2one("res.country.state", 'State'),
        	'country_id_correspond_client2': fields.many2one('res.country', 'Country'),
        	'country_correspond_client2': fields.related('country_id', type='many2one', relation='res.country', string='Country',
                                  deprecated="This field will be removed as of OpenERP 7.1, use country_id instead"),
		'profession_client2':fields.selection([('salaried','Salaried'),('self-employed','Self Employed'),('retired','Retired'),('homemaker','Home Maker')],'Business'),
		'designation_client2':fields.char('Designation',select=1),
		'company_name_client2':fields.char('Company name',select=1),
		'street_registration_client2': fields.char('Street', size=128),
        	'street2_registration_client2': fields.char('Street2', size=128),
        	'zip_registration_client2': fields.char('Postcode', change_default=True, size=24),
        	'city_registration_client2': fields.char('City', size=128),
        	'state_id_registration_client2': fields.many2one("res.country.state", 'State'),
        	'country_id_registration_client2': fields.many2one('res.country', 'Country'),
        	'country_registration_client2': fields.related('country_id', type='many2one', relation='res.country', string='Country',
                                  deprecated="This field will be removed as of OpenERP 7.1, use country_id instead"),
		'telephone_one_client2':fields.char('Telephone'),
		'fax_one_client2':fields.char('Fax'),
		'street_business_client2': fields.char('Street', size=128),
        	'street2_business_client2': fields.char('Street2', size=128),
        	'zip_business_client2': fields.char('Postcode', change_default=True, size=24),
        	'city_business_client2': fields.char('City', size=128),
        	'state_id_business_client2': fields.many2one("res.country.state", 'State'),
        	'country_id_business_client2': fields.many2one('res.country', 'Country'),
        	'country_rbusiness_client2': fields.related('country_id', type='many2one', relation='res.country', string='Country',
                                  deprecated="This field will be removed as of OpenERP 7.1, use country_id instead"),
		'telephone_two_client2':fields.char('Telephone'),
		'fax_two_client2':fields.char('Fax'),
		'email_client2': fields.char('Email Id', size=240),
		## Directors for Company
		'company_id_director':fields.many2one('suisse.client.general.info', 'All Directors'),
		'director_id': fields.one2many('suisse.client.general.info', 'company_id_director', 'Directors'),
		'name_of_director':fields.char('Name of Director',size=200),
		'director_cinnumber': fields.char('CIN Number', size=64,select=True),
		'mobile_director': fields.char('Mobile', size=64,select=True),
		'nationality_director': fields.many2one('res.country', 'Nationality'),
		'resident_status_director': fields.selection([('nonres','Non-Resident'),('resident','Resident')],'Residential status'),
		'date_of_birth_director': fields.date('Date of Birth'),
		'sex_director':fields.selection([('male','Male'),('female','Female')],'Sex'),
		'marital_status_director':fields.selection([('single','Single'),('married','Married'),('divorced','Divorced'),('separated','Separated'),('widowed','Widowed')],'Marital Status'),
		'date_of_relationship_director':fields.date('Date of Relationship',select=1),
		'passport_number_director':fields.char('Passport Number',select=True),
		'pass_validity_director':fields.date('Passport Validity'),
		'visa_expiry_director':fields.date('Visa Expiry'),
		'relationship_manager_director':fields.many2one('suisse.relationship.manager','Relationship Manager'),
		'street_correspond_director': fields.char('Street', size=128),
        	'street2_correspond_director': fields.char('Street2', size=128),
        	'zip_correspond_director': fields.char('Postcode', change_default=True, size=24),
        	'city_correspond_director': fields.char('City', size=128),
        	'state_id_correspond_director': fields.many2one("res.country.state", 'State'),
        	'country_id_correspond_director': fields.many2one('res.country', 'Country'),
        	'country_correspond_director': fields.related('country_id', type='many2one', relation='res.country', string='Country',
                                  deprecated="This field will be removed as of OpenERP 7.1, use country_id instead"),
		'profession_director':fields.selection([('salaried','Salaried'),('self-employed','Self Employed'),('retired','Retired'),('homemaker','Home Maker')],'Business'),
		'designation_director':fields.char('Designation',select=1),
		'company_name_director':fields.char('Company name',select=1),
		'street_registration_director': fields.char('Street', size=128),
        	'street2_registration_director': fields.char('Street2', size=128),
        	'zip_registration_director': fields.char('Postcode', change_default=True, size=24),
        	'city_registration_director': fields.char('City', size=128),
        	'state_id_registration_director': fields.many2one("res.country.state", 'State'),
        	'country_id_registration_director': fields.many2one('res.country', 'Country'),
        	'country_registration_director': fields.related('country_id', type='many2one', relation='res.country', string='Country',
                                  deprecated="This field will be removed as of OpenERP 7.1, use country_id instead"),
		'telephone_one_director':fields.char('Telephone'),
		'fax_one_director':fields.char('Fax'),
		'street_business_director': fields.char('Street', size=128),
        	'street2_business_director': fields.char('Street2', size=128),
        	'zip_business_director': fields.char('Postcode', change_default=True, size=24),
        	'city_business_director': fields.char('City', size=128),
        	'state_id_business_director': fields.many2one("res.country.state", 'State'),
        	'country_id_business_director': fields.many2one('res.country', 'Country'),
        	'country_business_director': fields.related('country_id', type='many2one', relation='res.country', string='Country',
                                  deprecated="This field will be removed as of OpenERP 7.1, use country_id instead"),
		'telephone_two_director':fields.char('Telephone'),
		'fax_two_director':fields.char('Fax'),
		'email_director': fields.char('Email Id', size=240),
		#Financial Details
		'occupation':fields.char('Occupation'),
		'regular_income_employment':fields.char('Regular Income From Employment'),
		'regular_income_self':fields.char('Regular Income From Self Employment'),
		'currency':fields.many2one('res.currency','Currency',select=True),
		'amount':fields.integer('Amount',select=True),
		'investment_held_for':fields.date('Date',select=True),
		'account_details':fields.one2many('fund.info','ac_details','Fund Details'),
		'prop_details':fields.one2many('property.info','property_information','Property Details'),
		#Company Details
		'company_name_gi3':fields.char('Company Name',select=True),
		'mobile_gi3':fields.char('Mobile Number'),
		'date_of_incorporation_gi3':fields.date('Date of Incorporation'),
		'registration_company_gi3':fields.char('Registration Company'),
		'passport_no_gi3':fields.char('Passport Number'),
		'validity_gi3':fields.date('Validity'),
		'lisence_no_gi3':fields.char('Lisence Number'),
		'validity_lisence_gi3':fields.date('Lisence Validity'),
		'street_gi3': fields.char('Street', size=128),
        	'street2_gi3': fields.char('Street2', size=128),
        	'zip_gi3': fields.char('Postcode', change_default=True, size=24),
        	'city_gi3': fields.char('City', size=128),
        	'state_id_gi3': fields.many2one("res.country.state", 'State'),
        	'country_id_gi3': fields.many2one('res.country', 'Country'),
		'telephone_gi3':fields.char('Telephone'),
		'fax_gi3':fields.char('Fax'),
		##Source of fund
		'source_of_fund':fields.many2one('suisse.client.general.info', 'All Source of Fund'),
		'source_of_fund_id': fields.one2many('suisse.client.general.info', 'source_of_fund', 'Source of funds'),
		'account_no_gi3':fields.char('Account Number'),
		'iban_gi3':fields.char('IBAN'),
		'street_bank_gi3': fields.char('Street', size=128),
        	'street2_bank_gi3': fields.char('Street2', size=128),
        	'zip_bank_gi3': fields.char('Postcode', change_default=True, size=24),
        	'city_bank_gi3': fields.char('City', size=128),
        	'state_id_bank_gi3': fields.many2one("res.country.state", 'State'),
        	'country_id_bank_gi3': fields.many2one('res.country', 'Country'),
		'swift_code_gi3':fields.char('Swift Code',select=True),
		'categories_banking_one':fields.one2many('categories.banking','client_categories_one','Categories Bank'),
		'categories_saving_plan':fields.one2many('categories.saving.plan','client_categories_saving','Categories Saving'),
		'categories_insurance_plan':fields.one2many('categories.insurance.plan','client_categories_insurance','Categories Insurance'),
		'categories_bond_plan':fields.one2many('categories.bond.plan','client_categories_bond','Categories Bond'),
		
	}
	def create(self, cr, uid, vals, context=None):
		if vals.get('name','/')== '/':
			vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'suisse.client.general.info') or '/'
		clients_no =  super(suisse_client_general_information, self).create(cr, uid, vals, context=context)
		return clients_no
	
	def write(self,cr,uid,ids,vals,context=None):
				
		if 'categories_bond_plan' in vals:
		   if vals['categories_bond_plan'][0][2]:
		   	if 'cat_bond_plan_no_one' in vals['categories_bond_plan'][0][2]:
			    cat_bond_plan_no_one = vals['categories_bond_plan'][0][2]['cat_bond_plan_no_one']
			    bond_obj=self.pool.get("categories.bond.plan")
			    val=bond_obj.onchange_bond_number(cr,uid,ids,cat_bond_plan_no_one)
			    vals['categories_bond_plan'][0][2]['datas_new']=val['value']['datas_new']
    
  
		if 'categories_insurance_plan'in vals:
		   if vals['categories_insurance_plan'][0][2]:
		   	if 'cat_insurance_policy_no_one' in vals['categories_insurance_plan'][0][2]:
			    cat_insurance_policy_no_one = vals['categories_insurance_plan'][0][2]['cat_insurance_policy_no_one']
			    insurance_obj=self.pool.get("categories.insurance.plan")
			    val=insurance_obj.onchange_insurance_number(cr,uid,ids,cat_insurance_policy_no_one)
			    vals['categories_insurance_plan'][0][2]['datas_new']=val['value']['datas_new']
		    
		if 'categories_saving_plan' in vals:
		   if vals['categories_saving_plan'][0][2]:
			   	if 'cat_policy_no_one' in  vals['categories_saving_plan'][0][2]:
				    cat_policy_no_one = vals['categories_saving_plan'][0][2]['cat_policy_no_one']
				    saving_obj=self.pool.get("categories.saving.plan")
				    val=saving_obj.onchange_policy_number(cr,uid,ids,cat_policy_no_one)
				    vals['categories_saving_plan'][0][2]['datas_new']=val['value']['datas_new']
		    
  		return super(suisse_client_general_information, self).write(cr, uid,ids,vals,context=None)
			

	def view_risk_profile(self,cr,uid,ids,context=None):
		'''
		This function returns an action that display investment risk profile of given client. It can either be a in a list or in a form view, if there is only one risk profile to show.
		'''
		mod_obj = self.pool.get('ir.model.data')

		for client in self.browse(cr, uid, ids, context=context):
                    vals={'relationship_title':client.id,'investment_client_one':client.name_of_client_one,
'investment_client_two':client.name_of_client_two}
	            new_id=self.pool.get('client.investment.risk.profile').create(cr,uid,vals)		
		
		value = {
                    'domain': str([('id', 'in', new_id)]),
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'client.investment.risk.profile',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'name' : _('Investment Risk Profile'),
                    'res_id': new_id
                }
           	return value

		

	_defaults={
		'image': lambda self, cr, uid, ctx={}: self.pool.get('res.partner')._get_default_image(cr, uid, False, ctx, colorize=True),
		'name': lambda obj, cr, uid, context: '/',
		'amount':0.00,
		'user_id': lambda obj, cr, uid, context: uid,
	}
	_order='name'

	

suisse_client_general_information()
class categories_banking(osv.osv):
	_name='categories.banking'
	
	_columns={
		'cat_private_banking_account_one':fields.char('Account Number',size=200),
		'cat_private_banking_bank_name_one':fields.selection([('ubs','UBS'),('lgt','LGT')],'Bank Name'),
		'client_categories_one':fields.many2one('suisse.client.general.info','Private Bank', select=True, ondelete='cascade'),	
	}

categories_banking()
class categories_saving_plan(osv.osv):
	
	_name='categories.saving.plan'
	 # 'data' field implementation
   	def _full_path(self, cr, uid, location, path):
		# location = 'file:filestore'
		assert location.startswith('file:'), "Unhandled filestore location %s" % location
		location = location[5:]

		# sanitize location name and path
		location = re.sub('[.]','',location)
		location = location.strip('/\\')

		path = re.sub('[.]','',path)
		path = path.strip('/\\')
		return os.path.join(tools.config['root_path'], location, cr.dbname, path)

    	def _file_read(self, cr, uid, location, fname, bin_size=False):
			full_path = self._full_path(cr, uid, location, fname)
			r = ''
			try:
			    if bin_size:
			        r = os.path.getsize(full_path)
			    else:
			        r = open(full_path,'rb').read().encode('base64')
			except IOError:
			    _logger.error("_read_file reading %s",full_path)
			return r

    	def _file_write(self, cr, uid, location, value):
			bin_value = value.decode('base64')
			fname = hashlib.sha1(bin_value).hexdigest()
			# scatter files across 1024 dirs
			# we use '/' in the db (even on windows)
			fname = fname[:3] + '/' + fname
			full_path = self._full_path(cr, uid, location, fname)
			
			try:
			    dirname = os.path.dirname(full_path)
			    if not os.path.isdir(dirname):
			        os.makedirs(dirname)
			    open(full_path,'wb').write(bin_value)
			except IOError:
			    _logger.error("_file_write writing %s",full_path)
			return fname

    	def _file_delete(self, cr, uid, location, fname):
			count = self.search(cr, 1, [('store_fname_name','=',fname)], count=True)
			if count <= 1:
			    full_path = self._full_path(cr, uid, location, fname)
			    try:
			        os.unlink(full_path)
			    except OSError:
			        _logger.error("_file_delete could not unlink %s",full_path)
			    except IOError:
			        # Harmless and needed for race conditions
			        _logger.error("_file_delete could not unlink %s",full_path)

    	def _data_get(self, cr, uid, ids, name, arg, context=None):
			#print ('Name is'),name
			#print ('Arg is'),arg
			if context is None:
			    context = {}
			result = {}
			location = self.pool.get('ir.config_parameter').get_param(cr, uid, 'ir_attachment.location')
			for attach in self.browse(cr, uid, ids, context=context):
			    #print ('Attachment is'),attach
			    if location and attach.store_fname_name:
			        result[attach.id] = self._file_read(cr, uid, location, attach.store_fname_name, bin_size)
			    else:
			        result[attach.id] = attach.db_datas_new
				#print ('Attachment id2 is'),result[attach.id]
			return result

    	def _data_set(self, cr, uid, id, name, value, arg, context=None):
			# We dont handle setting data to null
			if not value:
			    return True
			if context is None:
			    context = {}
			location = self.pool.get('ir.config_parameter').get_param(cr, uid, 'ir_attachment.location')
			file_size = len(value.decode('base64'))
			if location:
			    attach = self.browse(cr, uid, id, context=context)
			    if attach.store_fname_name:
			        self._file_delete(cr, uid, location, attach.store_fname_name)
			    fname = self._file_write(cr, uid, location, value)
			    
			    self.write(cr, uid, [id], {'store_fname_name': fname, 'file_size_new': file_size}, context=context)
			else:
			   
			    self.write(cr, uid, [id], {'db_datas_new': value, 'file_size_new': file_size}, context=context)
			return True

	
	_columns={
		'cat_provider_one':fields.selection([('generali','Generali'),('friends','Friends Provident International'),('zurich','Zurich'),('metlife','MetLife Alico'),('royal','Royal Skandia')],'Provider'),
		'cat_policy_no_one':fields.char('Plan Number',size=200),
		'client_categories_saving':fields.many2one('suisse.client.general.info','Saving Plans', select=True, ondelete='cascade'),
		'datas_new':fields.function(_data_get, fnct_inv=_data_set, string='File Content', type="binary", nodrop=True),
		'file_size_new': fields.integer('File Size'),
		'store_fname_name': fields.char('Stored Filename', size=256),
		'db_datas_new': fields.binary('Database Data'),
	}
	def onchange_policy_number(self,cr,uid,ids,cat_policy_no_one):
		if not cat_policy_no_one:
			raise osv.except_osv(_('You have not entered any Plan number'),_("Please Provide a Plan Number!!") )
		res ={'value':{'datas_new':''}}
		path='/home/chinna/Desktop/suisse_policy_doc'
   		new_path=os.getcwd()
   		os.chdir(os.path.expanduser(path))
   		dir2=os.getcwd()
		for pdf in os.listdir("."):
   			if (pdf== cat_policy_no_one +'.pdf'):
   				fop=open(dir2+'/'+pdf,'rb').read().encode('base64')
   				res['value'].update({'datas_new':fop})
		if not res['value']['datas_new']:
			raise osv.except_osv(_('There is no file with this plan number'),_("Place the related file with this plan number.") )
		
		return res
	
	
		

categories_saving_plan()

class categories_insurance_plan(osv.osv):
	_name='categories.insurance.plan'
	 # 'data' field implementation
   	def _full_path(self, cr, uid, location, path):
		# location = 'file:filestore'
		assert location.startswith('file:'), "Unhandled filestore location %s" % location
		location = location[5:]

		# sanitize location name and pat
		location = location.strip('/\\')

		path = re.sub('[.]','',path)
		path = path.strip('/\\')
		return os.path.join(tools.config['root_path'], location, cr.dbname, path)

    	def _file_read(self, cr, uid, location, fname, bin_size=False):
			full_path = self._full_path(cr, uid, location, fname)
			r = ''
			try:
			    if bin_size:
			        r = os.path.getsize(full_path)
			    else:
			        r = open(full_path,'rb').read().encode('base64')
			except IOError:
			    _logger.error("_read_file reading %s",full_path)
			return r

    	def _file_write(self, cr, uid, location, value):
			bin_value = value.decode('base64')
			fname = hashlib.sha1(bin_value).hexdigest()
			# scatter files across 1024 dirs
			# we use '/' in the db (even on windows)
			fname = fname[:3] + '/' + fname
			full_path = self._full_path(cr, uid, location, fname)
			
			try:
			    dirname = os.path.dirname(full_path)
			    if not os.path.isdir(dirname):
			        os.makedirs(dirname)
			    open(full_path,'wb').write(bin_value)
			except IOError:
			    _logger.error("_file_write writing %s",full_path)
			return fname

    	def _file_delete(self, cr, uid, location, fname):
			count = self.search(cr, 1, [('store_fname_name','=',fname)], count=True)
			if count <= 1:
			    full_path = self._full_path(cr, uid, location, fname)
			    try:
			        os.unlink(full_path)
			    except OSError:
			        _logger.error("_file_delete could not unlink %s",full_path)
			    except IOError:
			        # Harmless and needed for race conditions
			        _logger.error("_file_delete could not unlink %s",full_path)

    	def _data_get(self, cr, uid, ids, name, arg, context=None):
			#print ('Name is'),name
			#print ('Arg is'),arg
			if context is None:
			    context = {}
			result = {}
			location = self.pool.get('ir.config_parameter').get_param(cr, uid, 'ir_attachment.location')
			bin_size = context.get('bin_size')
			for attach in self.browse(cr, uid, ids, context=context):
			    #print ('Attachment is'),attach
			    if location and attach.store_fname_name:
			        result[attach.id] = self._file_read(cr, uid, location, attach.store_fname_name, bin_size)
			    else:
			        result[attach.id] = attach.db_datas_new
				#print ('Attachment id2 is'),result[attach.id]
			return result

    	def _data_set(self, cr, uid, id, name, value, arg, context=None):
			# We dont handle setting data to null
			if not value:
			    return True
			if context is None:
			    context = {}
			location = self.pool.get('ir.config_parameter').get_param(cr, uid, 'ir_attachment.location')
			file_size = len(value.decode('base64'))
			if location:
			    attach = self.browse(cr, uid, id, context=context)
			    if attach.store_fname_name:
			        self._file_delete(cr, uid, location, attach.store_fname_name)
			    fname = self._file_write(cr, uid, location, value)
			    self.write(cr, uid, [id], {'store_fname_name': fname, 'file_size_new': file_size}, context=context)
			else:
			    self.write(cr, uid, [id], {'db_datas_new': value, 'file_size_new': file_size}, context=context)
			return True

	
	_columns={
		'cat_insurance_provider_one':fields.selection([('salama','Salama'),('friends','Friends Provident International'),('zurich','Zurich'),('metlife','MetLife Alico')],'Provider'),
		'cat_insurance_policy_no_one':fields.char('Policy Number',size=200),
		'datas_new':fields.function(_data_get, fnct_inv=_data_set, string='File Content', type="binary", nodrop=True),
		'file_size_new': fields.integer('File Size'),
		'store_fname_name': fields.char('Stored Filename', size=256),
		'db_datas_new': fields.binary('Database Data'),
		'client_categories_insurance':fields.many2one('suisse.client.general.info','Insurance', select=True, ondelete='cascade'),
	}
	
	def onchange_insurance_number(self,cr,uid,ids,cat_insurance_policy_no_one):
		if not cat_insurance_policy_no_one:
			raise osv.except_osv(_('You have not entered any Plan number'),_("Please Provide a Plan Number!!") )
		res ={'value':{'datas_new':''}}
		path='/home/chinna/Desktop/suisse_policy_doc'
   		new_path=os.getcwd()
   		os.chdir(os.path.expanduser(path))
   		dir2=os.getcwd()
		for pdf in os.listdir("."):
   			if (pdf== cat_insurance_policy_no_one +'.pdf'):
   				fop=open(dir2+'/'+pdf,'rb').read().encode('base64')
   				res['value'].update({'datas_new':fop})
		if not res['value']['datas_new']:
			raise osv.except_osv(_('There is no file with this plan number'),_("Place the related file with this plan number.") )
		
		return res
	
categories_insurance_plan()
class categories_bond_plan(osv.osv):
	_name='categories.bond.plan'
	 # 'data' field implementation
   	def _full_path(self, cr, uid, location, path):
		# location = 'file:filestore'
		assert location.startswith('file:'), "Unhandled filestore location %s" % location
		location = location[5:]

		# sanitize location name and path
		location = re.sub('[.]','',location)
		location = location.strip('/\\')

		path = re.sub('[.]','',path)
		path = path.strip('/\\')
		return os.path.join(tools.config['root_path'], location, cr.dbname, path)

    	def _file_read(self, cr, uid, location, fname, bin_size=False):
			full_path = self._full_path(cr, uid, location, fname)
			r = ''
			try:
			    if bin_size:
			        r = os.path.getsize(full_path)
			    else:
			        r = open(full_path,'rb').read().encode('base64')
			except IOError:
			    _logger.error("_read_file reading %s",full_path)
			return r

    	def _file_write(self, cr, uid, location, value):
			bin_value = value.decode('base64')
			fname = hashlib.sha1(bin_value).hexdigest()
			# scatter files across 1024 dirs
			# we use '/' in the db (even on windows)
			fname = fname[:3] + '/' + fname
			full_path = self._full_path(cr, uid, location, fname)
			
			try:
			    dirname = os.path.dirname(full_path)
			    if not os.path.isdir(dirname):
			        os.makedirs(dirname)
			    open(full_path,'wb').write(bin_value)
			except IOError:
			    _logger.error("_file_write writing %s",full_path)
			return fname

    	def _file_delete(self, cr, uid, location, fname):
			count = self.search(cr, 1, [('store_fname_name','=',fname)], count=True)
			if count <= 1:
			    full_path = self._full_path(cr, uid, location, fname)
			    try:
			        os.unlink(full_path)
			    except OSError:
			        _logger.error("_file_delete could not unlink %s",full_path)
			    except IOError:
			        # Harmless and needed for race conditions
			        _logger.error("_file_delete could not unlink %s",full_path)

    	def _data_get(self, cr, uid, ids, name, arg, context=None):
			#print ('Name is'),name
			#print ('Arg is'),arg
			if context is None:
			    context = {}
			result = {}
			location = self.pool.get('ir.config_parameter').get_param(cr, uid, 'ir_attachment.location')
			bin_size = context.get('bin_size')
			for attach in self.browse(cr, uid, ids, context=context):
			    #print ('Attachment is'),attach
			    if location and attach.store_fname_name:
			        result[attach.id] = self._file_read(cr, uid, location, attach.store_fname_name, bin_size)
			    else:
			        result[attach.id] = attach.db_datas_new
				#print ('Attachment id2 is'),result[attach.id]
			return result

    	def _data_set(self, cr, uid, id, name, value, arg, context=None):
			# We dont handle setting data to null
			if not value:
			    return True
			if context is None:
			    context = {}
			location = self.pool.get('ir.config_parameter').get_param(cr, uid, 'ir_attachment.location')
			file_size = len(value.decode('base64'))
			if location:
			    attach = self.browse(cr, uid, id, context=context)
			    if attach.store_fname_name:
			        self._file_delete(cr, uid, location, attach.store_fname_name)
			    fname = self._file_write(cr, uid, location, value)
			    self.write(cr, uid, [id], {'store_fname_name': fname, 'file_size_new': file_size}, context=context)
			else:
			    self.write(cr, uid, [id], {'db_datas_new': value, 'file_size_new': file_size}, context=context)
			return True

	
	_columns={
		'cat_bond_provider_one':fields.selection([('generali','Generali'),('friends','Friends Provident International'),('zurich','Zurich'),('skandia','Skandia')],'Provider'),
		'cat_bond_plan_no_one':fields.char('Plan Number',size=200),
		'client_categories_bond':fields.many2one('suisse.client.general.info','Bonds', select=True, ondelete='cascade'),
		'datas_new':fields.function(_data_get, fnct_inv=_data_set, string='File Content', type="binary", nodrop=True),
		'file_size_new': fields.integer('File Size'),
		'store_fname_name': fields.char('Stored Filename', size=256),
		'db_datas_new': fields.binary('Database Data'),	
	}
	
	
	def onchange_bond_number(self,cr,uid,ids,cat_bond_plan_no_one):
		if not cat_bond_plan_no_one:
			raise osv.except_osv(_('You have not entered any Plan number'),_("Please Provide a Plan Number!!") )
		res ={'value':{'datas_new':''}}
		path='/home/chinna/Desktop/suisse_policy_doc'
   		new_path=os.getcwd()
   		os.chdir(os.path.expanduser(path))
   		dir2=os.getcwd()
		for pdf in os.listdir("."):
   			if (pdf== cat_bond_plan_no_one +'.pdf'):
   				fop=open(dir2+'/'+pdf,'rb').read().encode('base64')
   				res['value'].update({'datas_new':fop})
		if not res['value']['datas_new']:
			raise osv.except_osv(_('There is no file with this plan number'),_("Place the related file with this plan number.") )
		
		return res
categories_bond_plan()
class fund_details(osv.osv):
	_name='fund.info'
	
	_columns={
		'account_holder':fields.char('Account Holder'),
		'name_of_financial':fields.char('Name of Financial'),
		'ac_details':fields.many2one('suisse.client.general.info','Fund',select=True, ondelete='cascade'),
	}
fund_details()

class property_details(osv.osv):
	_name='property.info'
	
	_columns={
		'property_owned_country':fields.many2one('res.country', 'Country of Owned Property'),
		'street_property': fields.char('Street', size=128),
		'street2_property': fields.char('Street2', size=128),
		'zip_property': fields.char('Postcode', change_default=True, size=24),
		'city_property': fields.char('City', size=128),
		'state_id_property': fields.many2one("res.country.state", 'State'),
		'property_information':fields.many2one('suisse.client.general.info','Property',ondelete='cascade'),
	}
property_details()
class suisse_relationship_manager(osv.osv):
	_name = "suisse.relationship.manager"
	_rec_name ="name_of_relationship_manager"
	_columns={
		'name_of_relationship_manager':fields.char('Relationship Manager',size=200,select=True),
		'date_of_rm':fields.date('Creation Date'),
		'active':fields.boolean('Active'),
		'email':fields.char('Email',required=True),
		'login':fields.char('Username',size=64),
		'password':fields.char('Password',size=64),
		
	}
	_defaults = {
		'active':True,	
	}

	_order = "date_of_rm"
	
	def mail_relational_manager(self,cr,uid,id,context=None):
		mail_obj = self.pool.get('ir.mail_server').browse(cr,uid,uid,context)
		username = mail_obj.smtp_user
		password = mail_obj.smtp_pass
		host = mail_obj.smtp_host
		port = mail_obj.smtp_port
		fromaddr = username
		server = smtplib.SMTP(host+':'+'587')
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(username, password)
		msg = MIMEMultipart()
		msg['From'] = fromaddr
		msg['Subject'] = 'Regarding Account Details For SCAMC CRM'
		toaddr = id.email
		msg['To'] = toaddr
		text = ('<p><h2>Hello, %s</h2> Your account has been created in SCAMC CRM For Relationship Manager</p><p><b>Your login credentials are given below:-</b></p><p>Username:%s</p><p>Password:%s</p><p>To login click on below link</p><p><a href="http://77.245.179.5:8069">Click Here</a></p>')%(id.name_of_relationship_manager,id.login,id.password)
		body = MIMEText(text, _subtype='html')
		msg.attach(body)
		server.sendmail(fromaddr, toaddr, msg.as_string())
		server.quit()
		return True
	
	def create(self, cr, uid, vals, context=None):
		manager_no =  super(suisse_relationship_manager, self).create(cr, uid, vals, context=context)
		manager= self.browse(cr, uid, manager_no, context=context)
		if manager:
			val1={'name':manager.name_of_relationship_manager,'login': manager.login,'password':manager.password}
			new_id=self.pool.get('res.users').create(cr,uid,val1)
			self.mail_relational_manager(cr,uid,manager,context=None)
		return manager_no


suisse_relationship_manager()