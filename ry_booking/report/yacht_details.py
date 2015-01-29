import time

from openerp.report import report_sxw

class yacht(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(yacht, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time, 
        })
report_sxw.report_sxw('report.yatch.config', 'yatch.config', 'addons/ry_booking/report/yacht_details.rml', parser=yacht, header="external")
