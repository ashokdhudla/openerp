from openerp.osv import osv,fields
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient
import time
from tools import DEFAULT_SERVER_DATE_FORMAT
from  datetime import datetime



class crm_phone_call(osv.Model):
    _inherit = 'crm.opportunity2phonecall'
    
    def create_reminder(self,cr, uid, ids, context=None):
        opp_call_obj = self.browse(cr, uid, ids, context=context )
        pland_date = int(datetime.strptime(opp_call_obj[0].date, "%Y-%m-%d %H:%M:%S").strftime("%s")) * 1000
        
        eve_config_obj = self.pool.get('evernote.configuration')
        auth_token = eve_config_obj.browse(cr,uid,1,context=context).auth_token
        # new instance of Note with title and FPO content.
        note = Types.Note()
        client = EvernoteClient(token=auth_token)
        note_store = client.get_note_store()
        note.title = opp_call_obj[0].name
        note.content = """<?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
        """
        note.content += '<en-note>'
        note.content += opp_call_obj[0].note
        note.content += '</en-note>'
        now = int(round(time.time() * 1000))
        note.attributes = Types.NoteAttributes()
        note.attributes.reminderOrder = now
        note.attributes.reminderTime = pland_date
         
        try:
            createdNote = note_store.createNote(note)
        except Exception, e:
            print type(e)
            print e
            raise SystemExit
             
            print "Note created with GUID: %s" % createdNote.guid
#        createdNote.attributes.reminderDoneTime = int(round(time.time() * 1000))
        return True