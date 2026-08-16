from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    # Chapter 11
    _order = "price desc"

    # Chapter 10
    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "The offer price must be strictly positive.",
    )

    price = fields.Float(
        string="Price",
    )

    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
    )

    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=True,
    )

    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
    )

    # Chapter 11
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
    )

    # Chapter 8
    validity = fields.Integer(
        string="Validity",
        default=7,
    )

    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:

            date = (
                record.create_date
                or fields.Datetime.now()
            )

            record.date_deadline = (
                date.date()
                + timedelta(days=record.validity)
            )

    def _inverse_date_deadline(self):
        for record in self:

            date = (
                record.create_date
                or fields.Datetime.now()
            )

            if record.date_deadline:
                record.validity = (
                    record.date_deadline
                    - date.date()
                ).days

    # Chapter 9
    def action_accept(self):
        for record in self:

            if record.property_id.offer_ids.filtered(
                lambda offer:
                offer.status == "accepted"
                and offer != record
            ):
                raise UserError(
                    "Only one offer can be accepted."
                )

            record.status = "accepted"

            record.property_id.buyer_id = (
                record.partner_id
            )

            record.property_id.selling_price = (
                record.price
            )

        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"

        return True

    # Chapter 12
    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:

            property_id = vals.get(
                "property_id"
            )

            if not property_id:
                continue

            property_record = self.env[
                "estate.property"
            ].browse(property_id)

            highest_offer = max(
                property_record.offer_ids.mapped(
                    "price"
                ),
                default=0.0,
            )

            new_price = vals.get(
                "price",
                0.0,
            )

            if new_price < highest_offer:
                raise UserError(
                    "The offer must be higher than "
                    f"{highest_offer:.2f}"
                )

            property_record.state = (
                "offer_received"
            )

        return super().create(vals_list)