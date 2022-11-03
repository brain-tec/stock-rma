# Copyright 2022 ForgeFlow S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from odoo import api, fields, models


class RmaOrderLine(models.Model):
    _inherit = "rma.order.line"

    @api.depends(
        "move_ids",
        "move_ids.state",
        "move_ids.is_rma_scrap",
        "qty_scrap",
        "scrap_policy",
        "product_qty",
    )
    def _compute_qty_to_scrap(self):
        for rec in self:
            rec.qty_to_scrap = 0.0
            if rec.scrap_policy == "ordered":
                rec.qty_to_scrap = rec.product_qty - rec.qty_scrap
            elif rec.scrap_policy == "received":
                rec.qty_to_scrap = rec.qty_received - rec.qty_scrap

    @api.depends("move_ids", "move_ids.state", "move_ids.is_rma_scrap")
    def _compute_qty_in_scrap(self):
        product_obj = self.env["uom.uom"]
        for rec in self:
            qty = 0.0
            for move in self.env["stock.scrap"].search(
                [("origin", "=", rec.name), ("state", "=", "draft")]
            ):
                qty += product_obj._compute_quantity(move.scrap_qty, rec.uom_id)
            rec.qty_in_scrap = qty

    @api.depends("move_ids", "move_ids.state", "move_ids.is_rma_scrap")
    def _compute_qty_scrap(self):
        product_obj = self.env["uom.uom"]
        for rec in self:
            qty = 0.0
            for move in rec.move_ids.filtered(
                lambda m: m.state in ["done"] and m.is_rma_scrap
            ):
                qty += product_obj._compute_quantity(move.product_uom_qty, rec.uom_id)
            rec.qty_scrap = qty

    def _compute_scrap_count(self):
        for line in self:
            scraps = self.env["stock.scrap"].search([("origin", "=", line.name)])
            line.scrap_count = len(scraps)

    qty_to_scrap = fields.Float(
        string="Qty To Scrap",
        copy=False,
        digits="Product Unit of Measure",
        readonly=True,
        compute="_compute_qty_to_scrap",
        store=True,
    )
    qty_in_scrap = fields.Float(
        string="Qty In Scrap",
        copy=False,
        digits="Product Unit of Measure",
        readonly=True,
        compute="_compute_qty_in_scrap",
        store=True,
    )
    qty_scrap = fields.Float(
        string="Qty Scrap",
        copy=False,
        digits="Product Unit of Measure",
        readonly=True,
        compute="_compute_qty_scrap",
        store=True,
    )
    scrap_policy = fields.Selection(
        selection=[
            ("no", "Not required"),
            ("ordered", "Based on Ordered Quantities"),
            ("received", "Based on Received Quantities"),
        ],
        string="Scrap Policy",
        default="no",
        required=True,
        readonly=False,
    )
    scrap_count = fields.Integer(compute="_compute_scrap_count", string="# Scraps")

    @api.onchange("operation_id")
    def _onchange_operation_id(self):
        res = super(RmaOrderLine, self)._onchange_operation_id()
        if self.operation_id:
            self.scrap_policy = self.operation_id.scrap_policy or "no"
        return res

    def action_view_scrap_transfers(self):
        action = self.env.ref("stock.action_stock_scrap")
        result = action.sudo().read()[0]
        scraps = self.env["stock.scrap"].search([("origin", "=", self.name)])
        if len(scraps) > 1:
            result["domain"] = [("id", "in", scraps.ids)]
        elif len(scraps) == 1:
            res = self.env.ref("stock.stock_scrap_form_view", False)
            result["views"] = [(res and res.id or False, "form")]
            result["res_id"] = scraps.ids[0]
        return result
