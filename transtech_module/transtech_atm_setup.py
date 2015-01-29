from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime
import time
import urllib
import random

try:
    import simplejson as json
except ImportError:
    import json     # noqa

class atm_initial_setup(osv.osv):
	
	_name = "atm.info"


	def copy(self, cr, uid, id, default=None, context=None):
		if not default:
			default = {}
		default.update({
            'atm_code': self.pool.get('ir.sequence').get(cr, uid, 'atm.info'),
        })
		return super(atm_initial_setup, self).copy(cr, uid, id, default, context=context)



	_columns = {
		
		'atm_code':fields.char('ATM Code',readonly=True),
		'name':fields.char("ATM Branch Details",required=True),
		'atm_id':fields.char('Bank ATM ID(provided by Bank)', required=True),
		'atm_type':fields.selection([('atm_only','ATM only'),('atm_cash_deposit','ATM and Cash Deposit'), ('drive_through','Drive Through')],'ATM Type',required=True),
		'customer':fields.many2one('customer.info','Customer', required=True),
		'country':fields.many2one('res.country', 'Country', domain="[('code','=','AE')]"),
		'state_id':fields.many2one('res.country.state','State', required=True, domain="[('country_id','=',country)]"),
		'sla_start':fields.datetime('SLA Start Date',required=False),
		'sla_end':fields.datetime('SLA End Date', required=False),
		'no_of_visits':fields.char('Number of Visits', required=True),
		'comments':fields.text('Comments'),
		'longitude':fields.char('Longitude'),
		'latitude':fields.char('Latitude'),
        'child_ids': fields.one2many('atm.old','parent_id',string='Moves',readonly=True),
        'date':fields.date('Date'),
        'no_tasks':fields.integer('No. of Tasks',readonly=True)
		}

	def _default_country(self, cr, uid, context=None):
		cid = self.pool.get('res.country').search(cr, uid, [('code', '=', 'AE')], context=context)
		return cid[0]

	_defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d'),
        'country':_default_country,
    }

	_order = 'atm_code'


	def create(self, cr, uid, vals, context=None):
		if vals.get('atm_code','/')== '/':
			vals['atm_code'] = self.pool.get('ir.sequence').get(cr, uid, 'atm.info') or '/'
		return super(atm_initial_setup, self).create(cr, uid, vals, context=context)

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
            # if result:
            #     self.write(cr, uid, [partner.id], {
            #         'partner_latitude': result[0],
            #         'partner_longitude': result[1],
            #         'date_localization': fields.date.context_today(self,cr,uid,context=context)
            #     }, context=context)

	def name_get(self, cr, uid, ids, context=None):
	    if not len(ids):
	        return []
	    res = [(r['id'], r['name'] and '%s, %s' % (r['name'], r['atm_id']) or r['name'] ) for r in self.read(cr, uid, ids, ['name', 'atm_id'], context=context) ]
	    return res

	def onchange_customer(self,cr,uid,ids,customer,context=None):
		res={'value':{}}
		cust_obj = self.pool.get('customer.info').browse(cr,uid,customer)
		res['value'].update({'sla_start':cust_obj.sla_start,
			'sla_end':cust_obj.sla_end,
			'country':cust_obj.country_id.id})

		return res

	def count_tasks(self,cr,uid,context=None):
		tsk_ids = self.pool.get('atm.surverys.management').search(cr,uid,[('status','=','done')])
		t_obj = self.pool.get('atm.surverys.management').browse(cr,uid,tsk_ids)
		for i in t_obj:
			if i.status=='done':
				tsk_ids1 = self.pool.get('atm.surverys.management').search(cr,uid,[('atm','=',i.atm.id),('status','=','done')])
				self.pool.get('atm.info').write(cr,uid,i.atm.id,{'no_tasks':len(tsk_ids1)})
		return True


        
    	
atm_initial_setup()

class atm_old(osv.osv):
    _name = 'atm.old'    
    _columns = { 
    			'parent_id':fields.many2one('atm.info','ATM'),
                'longitude':fields.char('Longitude'),
				'latitude':fields.char('Latitude'),
                'date':fields.date('Date'),
                'name':fields.char("ATM Branch Details"),  
                }
atm_old
