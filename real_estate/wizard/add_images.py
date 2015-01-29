from openerp.osv import osv ,fields
from openerp.tools.translate import _

class add_images(osv.osv):
	_name = 'add.image'
	_description = "This is the wizard for add images"
	_columns = {
		"image" : fields.binary("Pic1",help="Listing Image"),
	}
add_images()