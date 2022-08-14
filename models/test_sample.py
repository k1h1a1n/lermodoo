
from odoo import models, fields

class LabSample(models.Model):
    _name = "lerm.testsample"

    entry = fields.Many2one("lerm.entry",strings="Entry")
    