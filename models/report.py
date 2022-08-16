from odoo import models, fields

class Report(models.Model):
    _name = "lerm.report"
    _rec_name = "notebook_id"
    notebook_id = fields.Many2one("lerm.notebook","Notebook")
    ulr_no = fields.Char("ULR NO")
    