# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    is_internal_ref = fields.Boolean(
        "Internal Reference", default=True)
    is_barcode = fields.Boolean(
        "Barcode", default=True)
    is_uom = fields.Boolean("UOM", default=True)
    

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_internal_ref = fields.Boolean(
        related="company_id.is_internal_ref", string="Internal Reference", readonly=False)
    is_barcode = fields.Boolean(
        related="company_id.is_barcode", string="Barcode", readonly=False)
    is_uom = fields.Boolean(
        related="company_id.is_uom", string="UOM", readonly=False)
    