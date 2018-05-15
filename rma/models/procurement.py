# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import api, fields, models


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    rma_line_id = fields.Many2one(
        comodel_name='rma.order.line', string='RMA line',
        ondelete="set null",
    )

    @api.multi
    def _get_stock_move_values(self):
        res = super(ProcurementOrder, self)._get_stock_move_values()
        for procurement in self:
            if self.rma_line_id:
                line = self.rma_line_id
                res['rma_line_id'] = line.id
                # Propagate partner_dest_id for proper drop-shipment reports.
                if procurement.partner_dest_id:
                    res['partner_id'] = procurement.partner_dest_id.id
                dest_loc = self.env["stock.location"].browse([
                    res["location_dest_id"]])[0]
                if dest_loc.usage == "internal":
                    res["price_unit"] = line.price_unit
        return res


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    rma_id = fields.Many2one(
        comodel_name='rma.order', string='RMA',
        ondelete="set null",
    )
    rma_line_id = fields.Many2one(
        comodel_name='rma.order.line', string='RMA line',
        ondelete="set null",
    )
