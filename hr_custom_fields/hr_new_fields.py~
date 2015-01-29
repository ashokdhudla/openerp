from openerp.osv import fields, osv
from openerp import  tools
class hr_custom_fields(osv.osv):

	#def _get_copy_image(self, cr, uid, ids, name, args, context=None):
    #    	result = dict.fromkeys(ids, False)
     #   	for obj in self.browse(cr, uid, ids, context=context):
     #       		result[obj.id] = tools.image_get_resized_images(obj.image)
     #  		return result
	
	#def _set_copy_image(self, cr, uid, id, name, value, args, context=None):
    #    	return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)

	_inherit = "hr.employee"
	_columns = {

	'emp_code':fields.char('Employee Code',size=200),
	#'firstname':fields.char('Firstname', size=50),
	#'lastname':fields.char('Lastname', size=50),
	#'middlename':fields.char('Middlename', size=50),
	'ref_no':fields.char('Employee Ref. No',size=200),
	'personal_no':fields.char('Personal No.', size=100),
	'labour_card_id_no':fields.char('Labour Card/ID No', size=60),
	'labour_card_issued_date':fields.date('Labour Card/ID IssuedDate'),
	'labour_card_expiry_date':fields.date('Labour Card/ID ExpiryDate'),
	'mobile_code':fields.char('Mobile Code', size=15),
	'preferred_name':fields.char('Preferred Name', size=64),
	'visa_no':fields.char('Visa No', size=50),
	'visa_type':fields.selection([('work_permit_visa', 'Work Permit Visa'),('mission_visa', 'Mission Visa')], 'Visa Type'),
	'landline_code':fields.char('Landline Code', size=20),
	'driving_license_id':fields.char('Driving License Id', size=50),
	'emirates_id':fields.char('Emirates Id Details', size=50),
	'visa_upload': fields.binary("Upload Your Visa Here", help="This field holds the image used as photo for the copy of visa & passport, limited to 1024x1024px."),
	'passport_upload': fields.binary("Upload Your Passport", help="This field holds the image used as photo for the copy of visa & passport, limited to 1024x1024px."),
	#'joining_date':fields.date("Joining Date"),

	}

hr_custom_fields()

