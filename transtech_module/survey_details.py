from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime
import time
from openerp import  tools
import random
import smtplib
class survey_details_info(osv.osv):
	_name="survey.info"


	def copy(self, cr, uid, id, default=None, context=None):
		if not default:
			default = {}
		default.update({
            'name': self.pool.get('ir.sequence').get(cr, uid, 'survey.info'),
        })
		return super(survey_details_info, self).copy(cr, uid, id, default, context=context)



	def _get_image(self, cr, uid, ids, name, args, context=None):
		print name
		result = dict.fromkeys(ids, False)
		print result
		for obj in self.browse(cr, uid, ids, context=context):
			print obj.id
                	if obj.bfr_img_front:
			    	result[obj.id] = tools.image_get_resized_images(obj.bfr_img_front)
				print result
				return result
			if obj.bfr_img_side:
		    		result[obj.id] = tools.image_get_resized_images(obj.bfr_img_side)
				return result
			if obj.bfr_img_back:
		    		result[obj.id] = tools.image_get_resized_images(obj.bfr_img_back)
				return result
			if obj.after_img_front:
		    		result[obj.id] = tools.image_get_resized_images(obj.after_img_front)
				return result
			if obj.after_img_side:
		    		result[obj.id] = tools.image_get_resized_images(obj.after_img_side)
				return result
			if obj.after_img_back:
		    		result[obj.id] = tools.image_get_resized_images(obj.after_img_back)
				return result
		
		
	def _set_image(self, cr, uid, id, name, value, args, context=None):
		if obj.bfr_img_front:
        		return self.write(cr, uid, [id], {'bfr_img_front': tools.image_resize_image_big(value)}, context=context)
		if obj.bfr_img_side:
			return self.write(cr, uid, [id], {'bfr_img_side': tools.image_resize_image_big(value)}, context=context)
		if obj.bfr_img_back:
			return self.write(cr, uid, [id], {'bfr_img_back': tools.image_resize_image_big(value)}, context=context)
		if obj.after_img_front:
			return self.write(cr, uid, [id], {'after_img_front': tools.image_resize_image_big(value)}, context=context)
		if obj.after_img_side:
			return self.write(cr, uid, [id], {'after_img_side': tools.image_resize_image_big(value)}, context=context)
		if obj.after_img_back:
			return self.write(cr, uid, [id], {'after_img_back': tools.image_resize_image_big(value)}, context=context)

	def _has_image(self, cr, uid, ids, name, args, context=None):
		result = {}
		for obj in self.browse(cr, uid, ids, context=context):
		    result[obj.id] = obj.bfr_img_front != False
		return result

	
	_columns={
       		"name":fields.char("Survey id",readonly=True),
		"surv_task":fields.many2one("atm.surverys.management",'ATM Report Task ID'),
		'month':fields.selection([
		    ('jan','Janauray'),
		    ('feb', 'February'),
		    ('mar', 'March'),
		    ('apr', 'April'),
		    ('may', 'May'),
		    ('june','June'),
		    ('jul', 'July'),
		    ('aug', 'August'),
		    ('sep', 'September'),
		    ('oct', 'October'),
		    ('nov', 'November'),
		    ('dec', 'December'),
		    ], 'Month'),
		'atm_surv':fields.many2one('atm.info','ATM'),
		'customer_surv':fields.many2one('customer.info','Customer'),
		'surveyor_surv':fields.many2one('res.users','Surveyor'),
		'remarks_survey':fields.many2one('remarks.category', 'Remarks Category'),
		'visit_tm':fields.datetime('Visit Time'),
		#"task_cust":fields.many2one('atm.surverys.management','Customer',domain="[('name','=',surv_task)]"),
		'bfr_img_front':fields.binary('Front View'),
		'bfr_img_side':fields.binary('Side View'),
		'bfr_img_back':fields.binary('Back View'),
		'after_img_front':fields.binary('Front View After'),
		'after_img_side':fields.binary('Side View After'),
		'after_img_back':fields.binary('Back View After'),
		'check_list1':fields.boolean('No Comments'),
		'check_list2':fields.boolean('Transactional Stickers faded'),
		'check_list3':fields.boolean('Collect Cash'),
		'check_list4':fields.boolean('Collect Receipt'),
		'check_list5':fields.boolean('Insert card'),
		'check_list6':fields.boolean('Insert cash'),
		'check_list7':fields.boolean('Network sticker'),
		'check_list8':fields.boolean('Instruction sticker'),
		'check_list9':fields.boolean('Vault branding'),
		'check_list10':fields.boolean('ATM ID'),
		'check_list11':fields.boolean('Cables securing'),
		'check_list12':fields.boolean('Trash bin'),
		'check_list13':fields.boolean('Trash bin keys'),
		'check_list14':fields.boolean('Side posters faded'),
		'check_list15':fields.boolean('Kiosk Surround maintenance'),
		'check_list16':fields.boolean('key Pad Displaced'),
		'check_list17':fields.boolean('Spot lights off'),
		'check_list18':fields.boolean('Decals'),
		'check_list19':fields.boolean('ATM Tower branding'),
		'check_list20':fields.boolean('Canopy branding'),
		'check_list21':fields.boolean('Surround Lock is damage/ Faulty'),
		'check_list22':fields.boolean('Spot Light is off'),
		'check_list23':fields.boolean('Main board Lights are off'),
		'check_list24':fields.boolean('Security Camera is out of focus'),
		'check_list25':fields.boolean('Security Camera cables are exposed'),
		'check_list26':fields.boolean('Out dated contact no on the ATM is still present'),
		'check_list27':fields.boolean('Network Sticker is faded'),
		'check_list28':fields.boolean('ATM Vault door found open'),
		'check_list29':fields.boolean('DED No on the ATM is found missing'),
		'cur_longitude':fields.char('Current Longitude'),
		'cur_latitude':fields.char('Current Latitude'),
		'nxt_survey_distance':fields.integer('Next Survey Distance'),
		'nxt_taskid':fields.many2one('atm.surverys.management','Next Task ID'),
		
		'image_medium': fields.function(_get_image, fnct_inv=_set_image,
		    string="Medium-sized image", type="binary", multi="_get_image",
		    store={
		        'survey.info': (lambda self, cr, uid, ids, c={}: ids, ['bfr_img_front'], 10),
			'survey.info': (lambda self, cr, uid, ids, c={}: ids, ['bfr_img_side'], 10),
			'survey.info': (lambda self, cr, uid, ids, c={}: ids, ['bfr_img_back'], 10),
			'survey.info': (lambda self, cr, uid, ids, c={}: ids, ['after_img_front'], 10),
			'survey.info': (lambda self, cr, uid, ids, c={}: ids, ['after_img_side'], 10),
			'survey.info': (lambda self, cr, uid, ids, c={}: ids, ['after_img_back'], 10),
		    },
		    help="Medium-sized image of this contact. It is automatically "\
		         "resized as a 128x128px image, with aspect ratio preserved. "\
		         "Use this field in form views or some kanban views."),	
		'image_small': fields.function(_get_image, fnct_inv=_set_image,
            		string="Small-sized image", type="binary", multi="_get_image",
            		store={
                	'survey.info': (lambda self, cr, uid, ids, c={}: ids, ['bfr_img_front'], 10),
			'survey.info': (lambda self, cr, uid, ids, c={}: ids, ['bfr_img_side'], 10),
			'survey.info': (lambda self, cr, uid, ids, c={}: ids, ['bfr_img_back'], 10),
			'survey.info': (lambda self, cr, uid, ids, c={}: ids, ['after_img_front'], 10),
			'survey.info': (lambda self, cr, uid, ids, c={}: ids, ['after_img_side'], 10),
			'survey.info': (lambda self, cr, uid, ids, c={}: ids, ['after_img_back'], 10),
           		 },
           		 help="Small-sized image of this contact. It is automatically "\
                	 "resized as a 64x64px image, with aspect ratio preserved. "\
                 	"Use this field anywhere a small image is required."),
        	'has_image': fields.function(_has_image, type="boolean"),
        'status': fields.selection([
		    ('waiting_approval','Waiting for Approval'),
		     ('approved','Approved')],'Status'),


       	}
	_order="name desc"

	_defaults={
	'status':'waiting_approval',
	'visit_tm': lambda * a: time.strftime('%Y-%m-%d %H:%M:%S'),
	}

	def onchange_taskid(self, cr, uid,ids,surv_task,context=None):
		res = {'value':{}}
		if surv_task:
			part = self.pool.get('atm.surverys.management').browse(cr, uid, surv_task, context)
			print part.atm.id
			res['value'].update({'month':part.task_month})
			res['value'].update({'atm_surv':part.atm.id})
			res['value'].update({'surveyor_surv':part.surveyor.id})
			
			res['value'].update({'customer_surv':part.customer.id})
			res['value'].update({'visit_tm':part.visit_time})
		
		return res

	def create(self,cr,uid,vals,context=None):
		vals['visit_tm']=datetime.datetime.now() 
		if vals.get('name','/') == '/': 
			vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'survey.info') or '/'
		print vals
		return super(survey_details_info, self).create(cr, uid, vals, context=context)


	def status_approve(self,cr,uid,ids,context=None):
		self.pool.get('survey.info').write(cr,uid,ids,{'status':'approved'})
		obj = self.browse(cr,uid,ids[0])
		self.pool.get('atm.surverys.management').write(cr, uid, obj.surv_task.id,{'status':'done'}, context)
		return True
	
	
	
survey_details_info()
