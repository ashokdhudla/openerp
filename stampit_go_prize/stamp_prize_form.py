from openerp.osv import osv,fields
from openerp.tools.translate import _
from datetime import datetime
import qrcode
from PIL import Image

class stampit_prize(osv.osv):
	_name="stamp.prize"
	_description = "StampIt Prize"
	_columns = {
		"code_name" : fields.char('Name Of Code',size=50,required=True,translate=True),
		"type_compition" : fields.char('Competition Type',size=80),
		"prize_one" : fields.char('Prize One',size=50),
		"prize_two" : fields.char('Prize Two',size=50),
		"prize_three" : fields.char('Prize Three',size=50),
		# "locality" : fields.many2one('locality.info','Locality',required=True),
		"start_date" : fields.date('Start Date'),
		"end_date" : fields.date('End Date'),
		"image" : fields.binary('Data'),
	}
	defaults = {
		# 'image' : generate_qrcode()
	}

	def generate_qrcode(self, cr, uid, ids, *args):
		res={}
		img = qrcode.make('ashok')
		print img
		img.show()
		# res.update({'img':img})
		#return {'value':res}
		return True


stampit_prize()


class prize_regusers(osv.osv):
	_name = "prize.regusers"
	_description = 'prize registration users'
	_columns = {
		"username" : fields.char('Username',size=100),
		"createdat" : fields.char('CreatedAt',size=100),
		"userid" : fields.char('UserId'),
	}
prize_regusers()