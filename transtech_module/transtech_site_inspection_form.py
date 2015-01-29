from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime
import time
from dateutil.relativedelta import relativedelta
from openerp import SUPERUSER_ID
class transtech_site_inspection(osv.osv):
	_name="transtech.site.inspection"

	def copy(self, cr, uid, id, default=None, context=None):
		if not default:
			default = {}
		default.update({
            'name': self.pool.get('ir.sequence').get(cr, uid, 'transtech.site.inspection'),
        })
		return super(atm_surverys_management, self).copy(cr, uid, id, default, context=context)

	_columns={
		'name':fields.char('Inspection ID', readonly=True),
        	'site_type':fields.selection([
		    ('ttw','TTW'),
		    ('lobby', 'LOBBY'),
		    ('other', 'Other'),
		    ('walkup', 'Walk UP'),
		    ('driveup', 'Drive UP'),
		    ], 'Site Type'),
                'surveyor':fields.many2one('res.users','Site Inspector Name',required=True),
		'date_assigned':fields.datetime('Date Assigned',required=True),
		'date_of_visit':fields.datetime('Date of Visit',required=True),
		'customer':fields.many2one('customer.info','Customer Name',size=64,required=True),
		'site_address':fields.text("Site Address"),
		'site_lat':fields.char("Latitude"),
		'site_long':fields.char("Longitute"),
		'contact_person':fields.char("Contact Person Name"),
		'contact_mobile':fields.char("Mobile Number"),
		'job_description':fields.text("Job Description"),
		'atm_brand':fields.char("ATM Brand/Model/Class"),
		'access_for_truck':fields.selection([('yes','Yes'),('no','No')],"Access For Truck"),
		'access_for_truck_crane':fields.selection([('yes','Yes'),('no','No')],"Access For Truck with Crane"),
		'hole_inside_height':fields.char("Hole Height from inside"),
		'inside_outside':fields.char("Hole Height from inside"),
		'hole_height':fields.char("Hole Height from Customer standing area"),
		'hole_height_outside':fields.char("Hole height from Outside"),
		
	}
	_order = "name desc"

	def create(self,cr,uid,vals,context=None):
		if vals.get('name','/') == '/': 
			vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'transtech.site.inspection') or '/'
		return super(transtech_site_inspection, self).create(cr, uid, vals, context=context)
		

	

transtech_site_inspection()



