
from odoo import models, fields

class TestParameter(models.Model):
    _name = "lerm.testparameter"
    _rec_name = 'name'
    group_id = fields.Many2one("lerm.testgroup",strings="Test Group")
    name = fields.Char(string="Parameter")
    min = fields.Integer("Min")
    max = fields.Integer("Max")
    method = fields.Many2one('lerm.method',string="Method")
