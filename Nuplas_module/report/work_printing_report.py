import time

from openerp.report import report_sxw

class work_printing(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(work_printing, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time, 
        })

report_sxw.report_sxw('report.packaging.board.printing', 'packaging.board.printing', 'addons/Nuplas_module/report/work_printing_report.rml', parser=work_printing, header="external")