
from openerp.osv import fields, osv

class TA_troubleshootdetails(osv.osv):
	
	def _serial_no(self,cr, uid, ids, field_name, arg, context=None):
		res={}
		
		counter = 0
		for i in self.browse(cr, uid, ids, context=context):
			res[i.id] = {
						'serial_number': 1,
			}
			counter = counter + 1
			res[i.id]['serial_number'] = counter
		return res
			
	_name ="ta.troubleshoot"	
	
	_columns ={
		'serial_number':fields.function(_serial_no,string='Sr. No',type='integer',multi="sums",readonly=True),
		'name':fields.char('Trouble Name',size=150, required=True),
		'module_name': fields.char("Module Name",size=150),
		'trouble_name': fields.text("Trouble Description"),
		'screen_shot' : fields.binary("ScreenShot"),
		'erp_name': fields.selection([('techanipr','TechAniprERP'),('incept','InceptERP'), ('unison','UnisonERP')],'ERP Name'),
		'change_given_by':fields.many2one('res.users',"Change Suggested By"),
		'priority_level' : fields.selection([('highest','Highest'),('medium','Medium'), ('low','Low')],'Priority Level'),
		'level_label' : fields.integer('Level Number'),
		'solution_type': fields.text("Solution"),
		'comments': fields.text("Comments"),
		'task':fields.boolean('Task'),
		
	}
	
	def onchange_task(self,cr,uid,ids,task,name,context=None):
		if task==True:
			project_id = self.pool.get('account.analytic.account').search(cr,uid,[('name','=','Troubleshoot')])
			pr_id = self.pool.get('project.project').search(cr,uid,[('analytic_account_id','=',project_id)])
		 	if project_id:
		 		val={'name':name,'project_id':pr_id[0]}
		 		return self.pool.get('project.task').create(cr,uid,val)
					
		return True
		

TA_troubleshootdetails()