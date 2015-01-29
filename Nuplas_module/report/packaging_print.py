import time

from openerp.report import report_sxw

class packaging_print(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(packaging_print, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time, 
        })

report_sxw.report_sxw('report.packaging.board', 'packaging.board', 'addons/Nuplas_module/report/packaging_print.rml', parser=packaging_print, header="external")