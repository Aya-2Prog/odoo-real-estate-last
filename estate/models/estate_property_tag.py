from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "The property tag name must be unique.",
    )

    name = fields.Char(
        string="Name",
        required=True,
    )

    # Chapter 11
    color = fields.Integer(
        string="Color",
    )