from openerp.osv import osv,fields
from openerp.tools.translate import _
from datetime import datetime
from PIL import Image

class transtech_imges(osv.osv):
	_name="transtech.img"
	_description = "Transtech Multi Images"

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
		'sl_no':fields.function(serial_inc,string='No',type="integer",multi="sums" ,readonly=True),
		'customer':fields.many2one('res.partner',"Customer",domain="[('customer','=',True)]"),
		"task_id" : fields.char('Task Id',size=50),
		"atmid_sys" : fields.char('Atm Id by sys',size=50),
		"atmid_bank" : fields.char('Atm Id by bank',size=50),
		'site_name' : fields.text('Site Name'),
		"no_visit" : fields.integer('No Of Visit'),
		"total_visit" : fields.integer('Total Visit'),
		"mis_visit" : fields.char('Mis Visit'),
	}
transtech_imges()
