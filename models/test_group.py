
from odoo import models, fields

class TestGroup(models.Model):
    _name = "lerm.testgroup"
    _rec_name = 'name'
    name = fields.Char("Name")
    parameters = fields.One2many("lerm.testgroup.parameter","testgroup_id",string="Parameter")
    



class TestGroupParams(models.Model):
    _name = "lerm.testgroup.parameter"
    _rec_name = 'parameters'
    testgroup_id = fields.Many2one("lerm.testgroup",string="Group")
    parameters = fields.Many2one("lerm.testparameter",string="Parameter")

    

class Method(models.Model):
    _name = "lerm.method"
    _rec_name = "name"
    code = fields.Char("Code")
    name = fields.Char("Name")
    determintion = fields.Char("Determinition")