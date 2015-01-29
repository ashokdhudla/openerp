
from openerp.osv import fields, osv

class res_partner_extend(osv.osv):
	_name ="res.partner"
	_inherit="res.partner"
	_columns ={
		'salutation':fields.char('Salutation',size=64),
		'first_name':fields.char('First Name',size=120),
		'last_name':fields.char('Last Name',size=120),
		'account_owners':fields.char('Account Owner',size=120),
		'account_names':fields.char('Account Name',size=120),
		
	}
	def create(self,cr,uid,vals,context=None):
		if vals['first_name']==False and vals['last_name']==False:
			vals.update({'name':'Demo1'})
			return super(res_partner_extend, self).create(cr, uid, vals, context=context)
		if(vals['first_name']==False):
			vals.update({'name':vals['last_name']})
			return super(res_partner_extend, self).create(cr, uid, vals, context=context)
		if(vals['last_name']==False):
			vals.update({'name':vals['first_name']})
			return super(res_partner_extend, self).create(cr, uid, vals, context=context)
		
		else:
			vals.update({'name':vals['first_name']+' '+vals['last_name']})
		return super(res_partner_extend, self).create(cr, uid, vals, context=context)
		
	def add_tags(self,cr,uid,ids,context=None):
		tag_search=self.search(cr,uid,[('name','!=',False),('category_id','=',False),('customer','=',True)])
		print tag_search
		category=self.pool.get('res.partner.category')
		category_ids=category.browse(cr,uid,[1],context=context)
		category_idnew= category_ids[0].id
		print category_idnew
		for cate1 in tag_search:
			print cate1
			print category_idnew
			cr.execute('insert into res_partner_res_partner_category_rel (category_id,partner_id) values (%s,%s)',(category_idnew,cate1))  
		return True
				
			
			
			
		
res_partner_extend()


