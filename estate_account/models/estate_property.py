from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for property_record in self:
            self.env["account.move"].create(
                {
                    "partner_id": property_record.buyer_id.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": property_record.name,
                                "quantity": 1.0,
                                "price_unit": property_record.selling_price * 0.06,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Administrative fees",
                                "quantity": 1.0,
                                "price_unit": 100.0,
                            }
                        ),
                    ],
                }
            )

        return super().action_sold()