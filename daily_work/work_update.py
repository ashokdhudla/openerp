from openerp.osv import fields, osv
class daily_work(osv.osv):
    
    _name="daily.work"
    
    _columns={
          'project_id':fields.related('project_id',type='many2one',relation='project.project',string='Project',store=True,required=True),
          'date':fields.date('Date',required=True),
          'user_id':fields.many2one('res.users','User', required=True),
          'desc':fields.char('Description',size=100),
          'duration':fields.float('Duration of Work'),
          'task':fields.many2one('project.task','Task',required=True),
          
              }
    
    _defaults = {
        'date': lambda self, cr, uid, ctx: ctx.get('date', fields.date.context_today(self,cr,uid,context=ctx)),
        'user_id': lambda obj, cr, uid, ctx: ctx.get('user_id') or uid,
    }
    
    def on_change_task(self, cr, uid,ids,task, context=None):
        res = {'value':{}}
        if task:
            r = self.pool.get('project.task').browse(cr, uid, task, context).project_id.id
            res['value'].update({'project_id':r})
            return res
        
        return res
        
    
    
daily_work()