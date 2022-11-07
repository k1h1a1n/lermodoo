from odoo import models ,fields
import logging

_logger = logging.getLogger(__name__)


class RejectReport(models.TransientModel):
    _name = "report.rejection.wizard"
    rejection_reason = fields.Text(string="Reason")


    def reject_report(self):
        report = self.env['lerm.report']
        notebook = self.env['lerm.notebook']
        report_id = self.env.context.get('active_id')
        report=report.search([('id','=',report_id)])
        notebook_id= report.notebook_id.id
        notebook=notebook.search([('id','=',notebook_id)])
        for wiz in self:
            rejection = wiz.rejection_reason
            notebook.message_post(body=rejection)
            notebook.write({
                'state':'rejected'
            })

            report.write({
                    'state':'2-rejected'
                })
        
        # notebook.write({

        # })

        
        
        # _logger.info("REJECT " + str(self.env.context.get('active_id')))
        # _logger.info("REJECT Reason " + str(report))
         
