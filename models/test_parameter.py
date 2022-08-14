
from odoo import models, fields

class LabSample(models.Model):
    _name = "lerm.testparameter"

    entry = fields.Many2one("lerm.entry",strings="Entry")
    