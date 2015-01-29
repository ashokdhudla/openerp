from openerp.osv import osv,fields
from openerp import tools
class gurukul_student_form(osv.osv):

	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
        	for obj in self.browse(cr, uid, ids, context=context):
            		result[obj.id] = tools.image_get_resized_images(obj.image)
        	return result
    
    	def _set_image(self, cr, uid, id, name, value, args, context=None):
        	return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)

	_name="gurukul.student"
	_columns={

	'name':fields.char('Name of the Student', size=64),
	'course':fields.char('Course'),
	'batch':fields.char('Batch'),
	'admission_no':fields.char('Admission No.'),
	'join_date':fields.date('Admission Date'),
	'date_of_birth':fields.date('Date of Birth'),
	'blood_group':fields.char('Blood Group'),
	'gender': fields.selection([('male', 'Male'),('female', 'Female')], 'Gender'),
	'country_id': fields.many2one('res.country', 'Nationality'),
	'language':fields.char('Language'),
	'category':fields.char('Category'),
	'religion':fields.char('Religion'),
	'address':fields.text('Address'),
	'city':fields.char('City'),
	'state': fields.many2one("res.country.state", 'State'),
	'zip_code':fields.char('Postal Code'),
	'country': fields.many2one('res.country', 'Country'),
	'phone':fields.char('Phone'),
	'mobile':fields.char('Mobile'),
	'sms_alerts':fields.boolean('Sms Alerts'),
	'email':fields.char('Email ID'),
	'image': fields.binary("Photo",
            help="This field holds the image used as photo for the student, limited to 1024x1024px."),
        'image_medium': fields.function(_get_image, fnct_inv=_set_image,
            string="Medium-sized photo", type="binary", multi="_get_image",
            store = {
                'hr.employee': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Medium-sized photo of the student. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved. "\
                 "Use this field in form views or some kanban views."),
        'image_small': fields.function(_get_image, fnct_inv=_set_image,
            string="Smal-sized photo", type="binary", multi="_get_image",
            store = {
                'hr.employee': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Small-sized photo of the student. It is automatically "\
                 "resized as a 64x64px image, with aspect ratio preserved. "\
                 "Use this field anywhere a small image is required."),

	}

gurukul_student_form()

