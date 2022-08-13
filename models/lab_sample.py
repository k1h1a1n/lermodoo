
from pyexpat import model
from odoo import models, fields

class LabSample(models.Model):
    _name = "lerm.sample"

    entry = fields.Many2one("lerm.entry",strings="Entry")
    