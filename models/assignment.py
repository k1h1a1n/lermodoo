from email.policy import default
from random import sample

from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)


class SampleAssignment(models.Model):
    _name = "sample.assignment"
    _rec_name = 'sample_id'
    sample_id = fields.Many2one("lerm.sample",string="Sample")
    responsible_technicians = fields.One2many("sample.assignment.technician","sample_assignment_id",string="Technicial")
    state = fields.Selection([('draft', 'Draft'),('assigned','Assigned')],default="draft",string="State")

    def button_confirm(self):

        for assignment in self:
            notebook = self.env['lerm.notebook'].create({
                                'sample': assignment.sample_id.id,
                                'assignment':self.id

                            })
            
            
            
            for parameter in assignment.sample_id.parameters:

                _logger.info("Params " +  str(parameter.parameter.id) + str(notebook.id) )
                
                self.env['lerm.notebook.result.entry'].create({
                                'notebook_id': notebook.id,
                                'parameter':parameter.parameter.id
                                

                            })

            self.write({'state': 'assigned' })




class SampleTechnicianAssignment(models.Model):
    _name = "sample.assignment.technician"
    sample_assignment_id = fields.Many2one("sample.assignment",string="Sample Assignment")
    technician = fields.Many2one("res.users","Technician")
    parameters = fields.Many2one("lerm.testparameter","Parameters")
    