from odoo import fields, models, api, _

class Website(models.Model):
    _inherit = 'website'

    price_visibility = fields.Selection([
        ('show','Show Price'),
        ('login','Login to view Price'),
        ('contact','Contact For Price'),
        ('','None')
        ],default='',string='Price Visibility',
        help='show product price Based on the selection.'			
	)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    price_visibility = fields.Selection(related='website_id.price_visibility', string="Check Layout", readonly=False)    