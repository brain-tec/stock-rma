# Copyright (C) 2017-20 ForgeFlow S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    auto_confirm_rma_sale = fields.Boolean(
        related="company_id.auto_confirm_rma_sale",
        string="Auto confirm Sales Order upon creation from RMA",
        help="When a sales is created from an RMA, automatically confirm it",
        readonly=False,
    )
    free_of_charge_rma_sale = fields.Boolean(
        related="company_id.free_of_charge_rma_sale",
        string="Free of charge RMA Sales Order",
        help="Sales orders created from RMA are free of charge by default",
        readonly=False,
    )
