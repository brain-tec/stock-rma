from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    auto_confirm_rma_sale = fields.Boolean(
        string="Auto confirm Sales Order upon creation from RMA",
        help="When a sales is created from an RMA, automatically confirm it",
    )
    free_of_charge_rma_sale = fields.Boolean(
        string="Free of charge RMA Sales Order",
        help="Sales orders created from RMA are free of charge by default",
        readonly=False,
    )
