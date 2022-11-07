from dataclasses import Field
from random import sample
from odoo import models, fields ,api
from odoo.exceptions import ValidationError
import logging

from soupsieve import comments

_logger = logging.getLogger(__name__)

class LabNotebook(models.Model):
    _name = "lerm.notebook"
    _rec_name = "sample"
    _inherit=['mail.thread','mail.activity.mixin'] 

    technical_manager = fields.Many2one("res.partner",domain=[('is_technical_manager','=',True)],string="Technical Manager")
    sample = fields.Many2one("lerm.sample","Sample")
    assignment = fields.Many2one('sample.assignment',string='Assignment')
    result_entry = fields.One2many("lerm.notebook.result.entry","notebook_id","Result Entry",tracking=True)
    comment = fields.Text(string="Comment")
    state = fields.Selection([('draft', 'Draft'),('approval','Appoval Pending'),('rejected','Rejected'),('published','Published')],default="draft",string="State")


    def button_confirm(self):

        if self.technical_manager:

            sequence = self.env['ulr.sequence'].search([])
            year = sequence.year
            report1 = self.env['lerm.report'].create({
                                'technical_manager': self.technical_manager.id,
                                'notebook_id': self.id,
                                'entry_id':self.sample.entry_id.id,
                                'year':year
                            })
            self.write({'state': 'approval' })
        
        else:
            raise ValidationError("Technical Manager is Required")



        



class LabNotebookResultEntry(models.Model):
    _name = "lerm.notebook.result.entry"
    notebook_id = fields.Many2one("lerm.notebook","Notebook")
    parameter = fields.Many2one("lerm.testparameter","Parameter")
    min = fields.Integer("Min",compute='_compute_min_max')
    max = fields.Integer("Max",compute='_compute_min_max')
    method = fields.Many2one("lerm.method",compute='_compute_min_max',string="Method")
    result = fields.Integer("Result")
    result_readonly = fields.Boolean('Results Readonly' ,compute='_compute_technician_access')
    remark = fields.Char("Remark")

    @api.depends('notebook_id.assignment',)
    def _compute_technician_access(self):
        context = self._context
        current_uid = context.get('uid')
        user_id = self.env['res.users'].browse(current_uid).id
        assignment_id =self.notebook_id.assignment.id
        #_logger.info("sample " +str(assignment_id))
        # search_tech = self.env['sample.assignment.technician'].search(['technician','=',user_id])
        search_tech = self.env['sample.assignment.technician'].search([('technician','=',user_id),('sample_assignment_id','=',assignment_id)])
        parameter_ids = []
      
        for i  in search_tech:
              _logger.info('naruto'+str(i.parameters.id))
              parameter_ids.append(i.parameters.id)

        


        for i in self:
            if(i.parameter.id in parameter_ids):
                i.result_readonly = False
            else:
                i.result_readonly = True



            


    @api.depends('parameter')
    def _compute_min_max(self):
        for entry in self:
            entry.min = entry.parameter.min
            entry.max = entry.parameter.max
            entry.method = entry.parameter.method.id
            print("lerm notebook printed 1")


            

