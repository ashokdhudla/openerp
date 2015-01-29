from openerp.osv import osv,fields

class mycompany_config(osv.osv):
	_name="company.info"
	_description="My company config"
	_columns = {
		'company_id' : fields.char('Company Id',size=50),
		'companyname' : fields.char('Company Name',size=120),
	}
	_rec_name = 'companyname'
mycompany_config()
class company_location(osv.osv):
	_name="company.location"
	_description = "Company Location"
	_columns = {
		'location_id' : fields.char('Location Id',size=50),
		'company_location' : fields.char('Company Location',size=100),
	}
company_location()