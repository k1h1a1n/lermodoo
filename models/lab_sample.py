
from pyexpat import model
from odoo import models, fields

class LabSample(models.Model):
    _name = "lerm.sample"
    _rec_name = "sample_no"
    entry_id = fields.Many2one("lerm.entry",strings="Entry")
    sample_no = fields.Char("Sample No.")
    product = fields.Many2one("product.template",domain=[('type','=','product')],strings="Sample")
    qty = fields.Integer("Qty")
    state = fields.Selection([('draft', 'Draft'),('confirmed','confirmed')],default="draft",string="State")
    groups = fields.One2many("lerm.sample.testgroup","sample_id","Test Group")
    parameters = fields.One2many("lerm.sample.parameter","sample_id",string="Parameters")

class SampleTestGroups(models.Model):
    _name = "lerm.sample.testgroup"
    sample_id = fields.Many2one("lerm.sample",string="Sample ID")
    group = fields.Many2one("lerm.testgroup",string="Test Group")

class SampleTestParameter(models.Model):
    _name = "lerm.sample.parameter"
    sample_id = fields.Many2one("lerm.sample",string="Sample ID")
    parameter = fields.Many2one("lerm.testparameter",string="Test Parameter")
    
