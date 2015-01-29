import time

from openerp.report import report_sxw

class yacht_bookings(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(yacht_bookings, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time, 
        })
report_sxw.report_sxw('report.booking.yachts', 'booking.yachts', 'addons/ry_booking/report/yacht_bookings.rml', parser=yacht_bookings, header="external")
