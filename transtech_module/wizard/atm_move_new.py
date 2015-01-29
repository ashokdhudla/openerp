from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
class atm_localization(osv.osv):
    _name = 'atm.move'   
    _columns = { 
                'longitude':fields.char('Longitude'),
				'latitude':fields.char('Latitude'),
                'date':fields.date('Date',readonly=True),
                'name':fields.char("ATM Branch Details"),  
                }


    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d')
    }

    def action_save(self,cr,uid,ids,context=None):
        atm_id = context['active_ids']
        data = self.read(cr, uid, ids)[0]
        atm_obj = self.pool.get('atm.info').browse(cr,uid,atm_id)[0]
        self.pool.get('atm.info').write(cr,uid,atm_id[0],{'child_ids':[[0, False, {'latitude': atm_obj.latitude, 'name': atm_obj.name, 'longitude': atm_obj.longitude,'date':atm_obj.date}]]},context=context)
        self.pool.get('atm.info').write(cr,uid,atm_id[0],data,context=context)
        #res = super(atm_localization,self).create(cr,uid,vals,context=None)
        return True


atm_localization()

class surveys_approve(osv.osv):
    _name="surveys.approve"

    def approve_survey(self, cr, uid, ids, context=None):
        data_inv = self.pool.get('survey.info').read(cr, uid, context['active_ids'], ['status'], context=context)

        for record in data_inv:
            if record['status'] not in ('waiting_approval'):
                raise osv.except_osv(_('Warning!'), _("Selected survey(s) cannot be approved as they are not in 'Waiting Approval' state."))
        self.pool.get('survey.info').write(cr,uid,context['active_ids'],{'status':'approved'})
        obj_list = self.pool.get('survey.info').browse(cr,uid,context['active_ids'])
        for obj in obj_list:
            self.pool.get('atm.surverys.management').write(cr, uid, obj.surv_task.id,{'status':'done'}, context)
        return {'type': 'ir.actions.act_window_close'}

surveys_approve()