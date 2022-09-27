from crypt import methods
from pickle import GET
from odoo import models, fields ,http,api
from odoo.http import request
import qrcode
import logging
import base64
from io import BytesIO


_logger = logging.getLogger(__name__)


class Report(models.Model):
    _name = "lerm.report"
    _rec_name = "notebook_id"
    _inherit=['mail.thread','mail.activity.mixin'] 

    notebook_id = fields.Many2one("lerm.notebook","Notebook")
    ulr_no = fields.Char("ULR NO")
    qr_code = fields.Binary("QR Code", attachment=True, store=True)


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