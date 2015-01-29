from openerp.osv import osv,fields
from  OpenERP_Evernote.create_evernote_atta import EvernoteUpload


class create_note_wizard(osv.TransientModel):
    
    _name='create.note.wizard'
    
    _columns = {
        'notebook' : fields.char('Notebook',size=128),
        'file': fields.char('PDF file', size=128),
    }
    
    def create_note(self, cr, uid, ids, context = None):
        proj_task_obj = self.pool.get('project.task')
        eve_config_obj = self.pool.get('evernote.configuration')
    
        try:
            auth_token = eve_config_obj.browse(cr,uid,1,context=context).auth_token
            data = self.browse(cr,uid,ids,context=context)
            project_task_data = proj_task_obj.browse(cr,uid,context.get('active_id'))
            ever_upload = EvernoteUpload(auth_token)
            ever_upload.upload_to_notebook(data[0].file, data[0].notebook)
            proj_task_obj.write(cr, uid, context.get('active_id'), {'note_created':1}, context=context)
        except:
                raise osv.except_osv(('Warning !'), ('Please check internet connection.!'))
      
        return True
        
        
#       S=s1:U=8d73f:E=14a51d649df:C=142fa251de1:P=1cd:A=en-devtoken:V=2:H=fd8d9c65b5588d666c04506049625399