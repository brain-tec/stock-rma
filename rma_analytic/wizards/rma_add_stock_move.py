# Copyright 2018 ForgeFlow S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import models


class RmaAddStockMove(models.TransientModel):
    _inherit = "rma_add_stock_move"

    def _prepare_rma_line_from_stock_move(self, sm, lot=False):
        data = super(RmaAddStockMove, self)._prepare_rma_line_from_stock_move(sm, lot)
        data.update(analytic_account_id=sm.analytic_account_id.id)
        return data
