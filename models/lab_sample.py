
from pyexpat import model
from odoo import models, fields

class LabSample(models.Model):
    _name = "lerm.sample"

    entry_id = fields.Many2one("lerm.entry",strings="Entry")
    sample_no = fields.Char("Sample No.")
    product = fields.Many2one("product.template",domain=[('type','=','sample')],strings="Sample")
    qty = fields.Integer("Qty")
    state = fields.Selection([('draft', 'Draft'),('confirmed','confirmed')],default="draft",string="State")

