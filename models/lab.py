from odoo import models, fields


class Lab(models.Model):
    _name = "lerm.entry"
    number = fields.Char("Number", required=True)
    date = fields.Date(string="Date", default=fields.Date.today)
    parties = fields.Many2one("res.partner", string="Parties", required=True)
    invoice_Parties = fields.One2many(
        "invoiceparty.details", "entry_id", string="Invoice Party", required=True
    )
    report_parties = fields.One2many(
        "reportparty.details", "entry_id", string="Report Party", required=True
    )
    acknowledgement_party = fields.One2many(
        "acknowldgementparty.details",
        "entry_id",
        string="Acknowledgement Party",
        required=True,
    )


class InvoiceParty(models.Model):
    _name = "invoiceparty.details"
    invoice_party = fields.Many2one(
        "res.partner", string="Invoice Party", required=True
    )
    entry_id = fields.Many2one("lerm.entry", string="Entry", required=True)


class ReportParty(models.Model):
    _name = "reportparty.details"
    report_party = fields.Many2one(
        "res.partner", string="Report Party", required=True)
    entry_id = fields.Many2one("lerm.entry", string="Entry", required=True)


class AcknowledgementParty(models.Model):
    _name = "acknowldgementparty.details"
    ack_party = fields.Many2one(
        "res.partner", string="Acknowledgement Party", required=True
    )
    entry_id = fields.Many2one("lerm.entry", string="Entry", required=True)


class ProductInheritedModel(models.Model):
    _inherit = "product.template"
    type = fields.Selection(selection=[("sample", "Sample"),("consu", "Consumable"),("service", "Service")])
