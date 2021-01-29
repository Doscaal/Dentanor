from odoo import api,fields,models

class ProductTemplate(models.Model):
	_inherit = 'product.template'

	price_visibility = fields.Selection([
			('show','Show Price'),
			('login','Login to view Price'),
			('contact','Contact For Price'),
			('',''),
		],default='',string='Price Visibility',)

	def get_price_visibility(self, website_id):
		self.ensure_one()
		if self.price_visibility:
			return self.price_visibility
		else:
			if website_id:
				return self.env['website'].sudo().search([('id','=',website_id)]).price_visibility
		return 'show'