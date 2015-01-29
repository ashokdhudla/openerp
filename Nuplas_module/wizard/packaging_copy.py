from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime
import time

class packaging_copy(osv.osv):

	_name="packaging.board.copy"

	# _columns={
	# 'reference':fields.char('Reference'),
	# }

	def package_copy_confirm(self, cr, uid, ids, context=None):
		print context
		default = {}
		for i in context['active_ids']:
			self.pool.get('packaging.board').copy(cr,uid,i,default=None,context=None)
		return {'type': 'ir.actions.act_window_close'}
	
packaging_copy()


class packaging_printing(osv.osv):

	_name="packaging.board.printing"
	_columns = {
					'no_copies': fields.char('No Of Copies'),
					'fields_name': fields.many2one('packaging.board','Work Order',required=True),
					'width_label' : fields.char('Width of Label'),
					'height_label': fields.char('Height of Label'),
					'cst' : fields.boolean('Work Order/Cst'),
					'cst1' : fields.char('Work Order/Cst1'),
					'color' : fields.boolean('Color'),
					'color1' : fields.char('Color1'),
					'gauge': fields.boolean('Guage'),
					'gauge1': fields.char('Guage1'),
					'mfg' : fields.boolean('Mfg'),
					'mfg1' : fields.char('Mfg1'),
					'exp' : fields.boolean('Exp'),
					'exp1' : fields.char('Exp1'),
				}
	_rec_name = 'fields_name'

	def create(self, cr, uid, vals, context=None):

		print "hello create method......"
		
		pack_obj = self.pool.get('packaging.board').browse(cr,uid,vals['fields_name'],context=None)
		if vals['mfg'] == True:
			vals.update({'mfg1':pack_obj.manufacture_date})
		if vals['color'] == True:
			vals.update({'color1':pack_obj.color})
		if vals['gauge'] == True:
			vals.update({'gauge1' : pack_obj.gauge})
		if vals['cst'] == True:
			vals.update({'cst1' : pack_obj.cst})
		if vals['exp'] == True:
			vals.update({'exp1' : pack_obj.expiry_date})
		print "valssss",vals
		return super(packaging_printing, self).create(cr, uid, vals, context=context)

	def printing_confirm_packaging(self,cr,uid,ids,context=None):
		data = self.read(cr, uid, ids)[0]
		valss = {}
		print data
		
		'''
		This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
		'''
		assert len(ids) == 1, 'This option should only be used for a single id at a time'
		datas = {
				'model': 'packaging.board.printing',
				'ids': ids,
				'form': self.read(cr, uid, ids[0], context=context),
			}
		print "datassss",datas
		return {'type': 'ir.actions.report.xml', 'report_name': 'packaging.board.printing', 'datas': datas, 'nodestroy': True}
		# data = self.read(cr, uid, ids)[0]
		# valss = {}
		# print data
		# packaging_id = data['fields_name']
		# print "idddddddd",packaging_id[0]
		# pack_obj = self.pool.get('packaging.board').browse(cr,uid,packaging_id[0],context=None)
		# valss.update({'fields_name':packaging_id[0]})
		# if data['mfg'] == True:
		# 	 valss.update({'mfg':pack_obj.manufacture_date})
		# else:
		# 	valss.update({'mfg':''})
		# if data['color'] == True:
		# 	valss.update({'color':pack_obj.color})
		# else:
		# 	valss.update({'color':''})
		# if data['gauge'] == True:
		# 	valss.update({'gauge' : pack_obj.gauge})
		# else:
		# 	valss.update({'gauge' : 0})
		# if data['cst'] == True:
		# 	valss.update({'cst' : pack_obj.cst})
		# else:
		# 	valss.update({'cst' : ''})
		# valss.update({'no_copies':data['no_copies']})
		# valss.update({'width_label':data['width_label']})
		# valss.update({'height_label':data['height_label']})
		# print "valsssss",valss
		# new_id = self.pool.get('packaging.board.printing').create(cr,uid,valss)
		# print "new_id",new_id
		# res = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'Nuplas_module', 'package_records_printing_confirm_tree')
		# res_id = res or res[1] or False
		# print "res_id",res_id[1]
		# return {
		# 	'type': 'ir.actions.act_window',
		# 	'name': 'packaging Label print',
		# 	'view_mode': 'tree',
		# 	'view_type': 'tree',
		# 	'view_id': res_id[1],
		# 	'res_model': 'packaging.board.printing',
		# 	'target': 'current',
		# 	'nodestroy': True,
		# 	'res_id': new_id or False,
		# 	'context': context,
		# }
	
packaging_printing()