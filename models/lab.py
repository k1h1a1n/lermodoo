from odoo import models, fields ,api
import logging

_logger = logging.getLogger(__name__)

class Lab(models.Model):
    _name = "lerm.entry"
    _rec_name = "number"
    _inherit=['mail.thread','mail.activity.mixin'] 
    number = fields.Char("Number", required=True)
    date = fields.Date(string="Date", default=fields.Date.today)
    parties = fields.Many2one("res.partner", string="Parties", required=True)
    # picking_type = fields.Many2one("stock.picking.type",string="Picking Type")
    supplier_location = fields.Many2one("stock.location", string="Supplier Location", required=True)
    internal_location = fields.Many2one("stock.location", string="Internal Location", required=True)
    product = fields.Many2one("product.template",string="Product")
    uom = fields.Many2one("uom.uom",string="UoM")
    invoice_Parties = fields.One2many(
        "invoiceparty.details", "entry_id", string="Invoice Party", required=True
    )

    samples = fields.One2many("lerm.sample", "entry_id", string="Samples")
    report_parties = fields.One2many(
        "reportparty.details", "entry_id", string="Report Party", required=True
    )
    acknowledgement_party = fields.One2many(
        "acknowldgementparty.details",
        "entry_id",
        string="Acknowledgement Party",
        required=True,
    )
    
    state = fields.Selection([('1-draft', 'Draft'),('2-confirmed','Confirmed')],default="1-draft",string="State")


    # @api.model
    # def create(self, values):
    #     _logger.info(values)
    #     new = super().create(values)
    #     return new

    def button_confirm(self):
        for entry in self:
            for sample in entry.samples:
                move1 = self.env['stock.move'].create({
                            'name': 'test_in_1',
                            'location_id': self.supplier_location.id,
                            'location_dest_id': self.internal_location.id,
                            'product_id': sample.product.id,
                            'product_uom': self.uom.id,
                            'product_uom_qty': sample.qty,
                            'state':'draft'
                        })
                move1._action_confirm()
                move_line = move1.move_line_ids[0]
                move_line.qty_done = sample.qty
                move1._action_done()
                vals = []
                for i in sample.parameters:
        #         _logger.info("Prod " + str(i.product_id))
                    data = (0, 0, {'parameters':i.parameter.id})
                    vals.append(data)
                self.env['sample.assignment'].create({

                            'sample_id': sample.id,
                            'responsible_technicians':vals
    
                        })
            

                
        
        
        # self.assertEqual(move1.state, 'draft')
       
        self.write({'state': '2-confirmed' })



    


class InvoiceParty(models.Model):
    _name = "invoiceparty.details"
    invoice_party = fields.Many2one(
        "res.partner", string="Invoice Party", required=True
    )
    entry_id = fields.Many2one("lerm.entry", string="Entry", required=True)


class ReportParty(models.Model):
    _name = "reportparty.details"
    report_party = fields.Many2one(
        "res.partner", string="Report Party", required=True)
    entry_id = fields.Many2one("lerm.entry", string="Entry", required=True)


class AcknowledgementParty(models.Model):
    _name = "acknowldgementparty.details"
    ack_party = fields.Many2one(
        "res.partner", string="Acknowledgement Party", required=True
    )
    entry_id = fields.Many2one("lerm.entry", string="Entry", required=True)


class ProductInheritedModel(models.Model):
    _inherit = "product.template"
    test_groups = fields.One2many('product.template.testgroup','product_template_id')
    # type = fields.Selection(selection=[("consu", "Consumable"),("service", "Service"),("product", "Storable Product")])
    
class ProductTestGroup(models.Model):
    _name = "product.template.testgroup"
    product_template_id = fields.Many2one('product.template',string="Product ID")
    test_group = fields.Many2one('lerm.testgroup',string="Test Group")
# class