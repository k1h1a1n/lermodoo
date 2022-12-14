from odoo import models , api

class NotebookReport(models.AbstractModel):
    _name = 'report.lermodoo.test_report_id_template'
    _description = 'Pdf data for notebook'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs1 = self.env['lerm.report'].browse(docids)
        docs = docs1[0].notebook_id.result_entry
        data = docs1[0].ulr_no
        print(data , "this is dodcs")

        return {
              'doc_ids': docids,
              'doc_model': 'lerm.report',
              'docs': docs,
              'data': docs1,
        }
