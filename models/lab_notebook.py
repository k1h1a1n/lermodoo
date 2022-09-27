from dataclasses import Field
from odoo import models, fields ,api


class LabNotebook(models.Model):
    _name = "lerm.notebook"
    _rec_name = "sample"
    _inherit=['mail.thread','mail.activity.mixin'] 

    sample = fields.Many2one("lerm.sample","Sample")
    result_entry = fields.One2many("lerm.notebook.result.entry","notebook_id","Result Entry")

    state = fields.Selection([('draft', 'Draft'),('published','Published')],default="draft",string="State")


    def button_confirm(self):
        report1 = self.env['lerm.report'].create({
                            'notebook_id': self.id,
                        })
        self.write({'state': 'published' })
        



class LabNotebookResultEntry(models.Model):
    _name = "lerm.notebook.result.entry"
    notebook_id = fields.Many2one("lerm.notebook","Notebook")
    parameter = fields.Many2one("lerm.testparameter","Parameter")
    min = fields.Integer("Min",compute='_compute_min_max')
    max = fields.Integer("Max",compute='_compute_min_max')
    method = fields.Many2one("lerm.method",compute='_compute_min_max',string="Method")
    result = fields.Integer("Result")
    remark = fields.Char("Remark")

    @api.depends('parameter')
    def _compute_min_max(self):
        for entry in self:
            entry.min = entry.parameter.min
            entry.max = entry.parameter.max
            entry.method = entry.parameter.method.id
            print("lerm notebook printed")


            

