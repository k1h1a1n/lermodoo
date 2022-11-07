
from pyexpat import model
from odoo import models, fields ,api
import logging

_logger = logging.getLogger(__name__)
class LabSample(models.Model):
    _name = "lerm.sample"
    _rec_name = "sample_no"
    _inherit=['mail.thread','mail.activity.mixin'] 
    entry_id = fields.Many2one("lerm.entry",strings="Entry")
    sample_no = fields.Char("Sample No.")
    product = fields.Many2one("product.template",domain=[('type','=','product')],strings="Sample")
    qty = fields.Integer("Qty")
    state = fields.Selection([('draft', 'Draft'),('confirmed','confirmed')],default="draft",string="State")
    groups = fields.One2many("lerm.sample.testgroup","sample_id","Test Group")
    parameters = fields.One2many("lerm.sample.parameter","sample_id",string="Parameters")


    def update_parameter(self):
       
        for record in self:
            param_ids = []
            already_exist_ids = []
            for test_group in record.groups:

                for i in self.parameters.parameter:
                     already_exist_ids.append(i.id)

                _logger.info(str(already_exist_ids))               

                for parameter in test_group.group.parameters:
                    
                    _logger.info(str(parameter.id in already_exist_ids))
                    
                    if parameter.id in already_exist_ids:
                       pass
                    else:
                        self.write({
                                'parameters': [
                                    (0,0, {'parameter': parameter.id })
                                ]
                            })
                    # _logger.info(parameter)



    # @api.model
    # def create(self, values):

    #     _logger.info(values)
    #     # values["parameters"] = [(0, 0, {})]
    #     # values["parameters"].append(0, 0, {'group':1})
    #     new = models.Model.create(self,values)

    #     return new

class SampleTestGroups(models.Model):
    _name = "lerm.sample.testgroup"
    sample_id = fields.Many2one("lerm.sample",string="Sample ID")
    group = fields.Many2one("lerm.testgroup",string="Test Group")


    @api.onchange("group")
    def set_domain_for_group(self):

        ids_already_in_group = []
        
        group_ids = []
        
        for group in self.sample_id.groups:
            ids_already_in_group.append(group.group.id)
        

        _logger.info("already" + str(ids_already_in_group))

        for group in self.sample_id.product.test_groups:

            if group.test_group.id in ids_already_in_group:
                ids_already_in_group.remove(group.test_group.id)
            else:
                group_ids.append(group.test_group.id)

        _logger.info("SASA "+ str(group_ids))
            
        

        _logger.info("sasa "+str(self.sample_id.product.test_groups))
        result = { 
                    'domain': {'group': [ 
                    ('id', 'in', group_ids)] 
                    } 
                 } 

        return result

class SampleTestParameter(models.Model):
    _name = "lerm.sample.parameter"
    sample_id = fields.Many2one("lerm.sample",string="Sample ID")
    parameter = fields.Many2one("lerm.testparameter",string="Test Parameter")
    
