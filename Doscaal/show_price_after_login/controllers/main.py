from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.http_routing.models.ir_http import slug

class WebsiteSale(WebsiteSale):
	@http.route(['/shop/cart/update'], type='http', auth="public", methods=['GET', 'POST'], website=True, csrf=False)
	def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
		product_template = request.env['product.product'].sudo().browse(int(product_id)).product_tmpl_id
		price_visibility = product_template.get_price_visibility(request.website.id)

		if price_visibility == 'contact':
			company = request.env['res.company'].sudo()._company_default_get('show_price_after_login')			
			return http.local_redirect('mailto:%s?subject=Price for %s'%(company.email,product_template.name))

		elif price_visibility == 'login' and request.env.user == request.website.user_id:
			return http.local_redirect('/web/login?redirect=/shop/product/%s'%slug(product_template))

		return super(WebsiteSale, self).cart_update(product_id, add_qty, set_qty, **kw)