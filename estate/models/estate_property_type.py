from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    # Chapter 11
    _order = "sequence, name"

    # Chapter 10
    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "The property type name must be unique.",
    )

    # Chapter 11
    sequence = fields.Integer(
        string="Sequence",
        default=1,
    )

    name = fields.Char(
        string="Name",
        required=True,
    )

    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
        string="Properties",
    )

    # Chapter 11 stat button
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
        string="Offers",
    )

    offer_count = fields.Integer(
        string="Offer Count",
        compute="_compute_offer_count",
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(
                record.offer_ids
            )