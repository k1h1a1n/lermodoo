from crypt import methods
import imp
from itertools import count
from pickle import GET
from symbol import parameters
from odoo import models, fields ,http,api
from odoo.http import request
import qrcode
import logging
import base64
from io import BytesIO
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class Report(models.Model):
    _name = "lerm.report"
    _rec_name = "notebook_id"
    _inherit=['mail.thread','mail.activity.mixin'] 
    
    entry_id = fields.Many2one("lerm.entry","Entry")
    notebook_id = fields.Many2one("lerm.notebook","Notebook")
    technical_manager = fields.Many2one("res.partner","Technical Manager")
    publish_reject_readonly = fields.Boolean('Results Readonly',compute="_compute_technical_manager_access")

    year = fields.Char("Year")
    ulr_no = fields.Char("ULR NO")
    qr_code = fields.Binary("QR Code", attachment=True, store=True)
    state = fields.Selection([('1-approval','Pending for Approval'),('2-rejected','Rejected'),('3-publish','Published')],default="1-approval",string="State")


    @api.depends('notebook_id')
    def _compute_technical_manager_access(self):
        context = self._context
        current_uid = context.get('uid')
        user_id = self.env['res.users'].browse(current_uid)
        _logger.info("Related Partner" +str(user_id.partner_id.id))
        for i in self:
            if i.technical_manager.id == user_id.partner_id.id:
                i.publish_reject_readonly = False
            else:
                 i.publish_reject_readonly = True


    
    

    def send_mail_customer(self):
        
        template_id = self.env.ref('lermodoo.report_to_customers').id

        ctx = {
            'default_model': 'lerm.report',
            'default_template_id': template_id,
        }
        
        
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx
        }
    
    def unlink(self):
        raise ValidationError("Cannot Delete")

        return super(Report, self).unlink()

    @api.model
    def create(self, values):
        new = super().create(values)
        url =  'http://localhost:8072/report?id='+str(new.id)
        # pdf, _ = request.env.ref('lermodoo.report_result')._render_qweb_pdf(kw['id'])
        qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=10,border=4)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image()
        temp = BytesIO()
        img.save(temp, format="PNG")
        qr_image = base64.b64encode(temp.getvalue())
        new.qr_code = qr_image
        print("create")
        return new
    
    def button_reject(self):
        self.notebook_id.write({'state':'rejected'})
        self.write({'state': '2-rejected' })
    
    def approval_confirm(self):
        self.notebook_id.write({'state':'published'})
        sequence = self.env['ulr.sequence'].search([])
        acc_no = sequence.accredition_no
        year = sequence.year
        loc = sequence.location
        check_parameter = sequence.within_param
        count = self.env['lerm.report'].search_count([('year','=',year)])
        report_sequences = count
        report_sequences = str(report_sequences).zfill(8)
        ulr_no = acc_no+"/"+year+"/"+loc+"/"+report_sequences+"/"+check_parameter
        _logger.info(sequence.accredition_no)

        self.write({'state': '3-publish','ulr_no': ulr_no })

    # @api.onchange('default_id')
    # def generate_qr_code(self):
    #     qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=10,border=4)
    #     qr.add_data(self.id)
    #     qr.make(fit=True)
    #     img = qr.make_image()
    #     temp = BytesIO()
    #     img.save(temp, format="PNG")
    #     qr_image = base64.b64encode(temp.getvalue())
    #     self.qr_code = qr_image

class UlrSequence(models.Model):
     _name = "ulr.sequence"
     accredition_no = fields.Char(string='Accredition No', size=6, required=True)
     year = fields.Char(string='Year', size=2, required=True)
     location = fields.Char(string='Location', size=1, required=True)
     within_param = fields.Char(string='Parameter', size=1, required=True)

class ReportController(http.Controller):
    @http.route('/report' ,method=["POST","GET"],csrf=False, type='http',auth='public')
    def index(self ,**kw):
        # request = request.jsonrequest
        _logger.info(kw)
        print("report controller")
        # url =  'http://localhost:8072/report?id='+str(kw['id'])
        pdf, _ = request.env.ref('lermodoo.report_result')._render_qweb_pdf(int(kw['id']))
        print(pdf ,"Tbis is PDF")
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', u'%s' % len(pdf))]
        return request.make_response(pdf, headers=pdfhttpheaders)