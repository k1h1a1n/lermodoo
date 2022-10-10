from odoo import models ,fields



class RejectReport(models.TransientModel):
    _name = "report.rejection.wizard"
    rejction_reason = fields.Text(string="Reason")