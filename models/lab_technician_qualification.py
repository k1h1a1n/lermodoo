from odoo import models, fields


class LabTechnician(models.Model):
    _inherit = "res.partner"
    is_technician = fields.Boolean("Technician")
    is_technical_manager = fields.Boolean("Technical Manager")


class LabTechnicianQualification(models.Model):
    _name = "lab.technician.qualification"
    _rec_name = 'technician'

    technician = fields.Many2one("res.partner",domain=[('is_technician','=',True)])
    methods = fields.One2many("lab.technician.qualification.method","technician_qualification_id",string="Methods")

class LabTechnicianQualificationMethod(models.Model):
    _name = "lab.technician.qualification.method"
    
    technician_qualification_id = fields.Many2one("lab.technician.qualification",string="ID")
    method = fields.Many2one("lerm.method",string="Method")