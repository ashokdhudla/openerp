from openerp.osv import fields, osv
from openerp import  tools

class fleet_custom_fields(osv.osv):
	
	_inherit = "fleet.vehicle"
	_columns = {

	'Registration_No':fields.char('Registration No',size=64,required=True),
	'Make':fields.char('Make',size=64,required=True),
	'Color':fields.char('Color',size=64,required=True),
	'Type_Of_Body':fields.char('Type Of Body',size=64,required=True),
	'Chassis_No':fields.char('Chassis No',size=64,required=True),
	'Engine_No':fields.char('Engine No',size=64,required=True),
	'Manufacture' : fields.char('Manufactureo',size=64,required=True),
	'Rating':fields.char('Rating',size=64,required=True),
	'Capacity':fields.char('Capacity',size=64,required=True),
	}

fleet_custom_fields()

class fleet_custom_fuel_fields(osv.osv):
	_inherit = 'fleet.vehicle.log.fuel'
	_columns={
		'Start_Date' : fields.date('Start Date',required=True),
		'End_Date' : fields.date('End Date',required=True),
		'Start_Millage' : fields.char('Start Millage',size=60,required=True),
		'End_Millage' : fields.char('End Millage',size=60,required=True),
		'Total_kilometres' : fields.char('Total kilometres',size=60,required=True),
		'Start_Date_and_time' : fields.datetime('Start Date and time',required=True),
		'End_Date_and_time' : fields.datetime('End Date and time',required=True),
		'Petrol_purchase_in_Litres' : fields.boolean('Petrol purchase in Litres'),
		'diesel_purchase_in_Litres' : fields.boolean('Diesel purchase in Litres'),
		'Sign' : fields.char('sign',size=50,required=True),
		'Driver_Name' : fields.many2one('res.partner','Driver Name',required=True),
	} 
fleet_custom_fuel_fields()

class fleet_custom_service_fields(osv.osv):
	_inherit = "fleet.vehicle.log.services"
	_columns = {
		'Time_In' : fields.char('Time In',size=30,required=True),
		'Next_Repair' : fields.date('Next Repair'),
		'Time_Out' : fields.char('Time Out',size=30,required=True),
		'Speedometer' : fields.char('Speedometer',size=30,required=True),
		'Garage_Mechanic' : fields.char('Garage Mechanic',size=30,required=True),
		'Nature_of_Repairs_Service' : fields.char('Nature of Repairs Service',size=30,required=True),
		'Signature' : fields.char('Signature',size=30,required=True),		
	}

fleet_custom_service_fields()


