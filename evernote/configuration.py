from openerp.osv import fields,osv

class evernote_configuration(osv.osv_memory):
    
    _name = 'evernote.configuration' 
    
    _columns = {
                'name': fields.char('Account Name', size=64),
                'username' : fields.char('Username',size=64),
                'passwd' : fields.char('Password',size=64),
                'auth_token': fields.char('Auth Token',size=128)
    }
    
    def add_connection(self,cr,uid,ids,context=None):
        data = self.browse(cr,uid,ids,context=context)
        vals={
              'name':data.name,
              'username':data.username,
              'passwd' : data.passwd,
              'auth_token':data.auth_token
        }
        self.write(cr, uid, ids[0],vals, context=context)
        