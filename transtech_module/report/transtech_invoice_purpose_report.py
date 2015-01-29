# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2005-2006 CamptoCamp
# Copyright (c) 2006-2010 OpenERP S.A
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
##############################################################################

import time
from openerp.report import report_sxw
#from common_report_header import common_report_header

class transtech_atm_info_invoice_purpose(report_sxw.rml_parse):
    _name = 'report.atm.info.invoice.purpose'

    def set_context(self, objects, data, ids, report_type=None):
        new_ids = ids
        #obj_move = self.pool.get('atm.info')
        #self.sortby = data['form'].get('sortby', 'sort_date')
        #self.query = obj_move._query_get(self.cr, self.uid, obj='l', context=data['form'].get('used_context',{}))
       # ctx2 = data['form'].get('used_context',{}).copy()
       # self.init_balance = data['form'].get('initial_balance', True)
        #if self.init_balance:
         #   ctx2.update({'initial_bal': True})
       # self.init_query = obj_move._query_get(self.cr, self.uid, obj='l', context=ctx2)
       # self.display_account = data['form']['customer']
       # self.target_move = data['form'].get('target_move', 'all')
        #ctx = self.context.copy()
        ctx['fiscalyear'] = data['form']['fiscalyear_id']
        if data['form']['filter'] == 'filter_period':
            ctx['periods'] = data['form']['periods']
        elif data['form']['filter'] == 'filter_date':
            ctx['date_from'] = data['form']['date_from']
            ctx['date_to'] =  data['form']['date_to']
        ctx['state'] = data['form']['target_move']
        self.context.update(ctx)
        if (data['model'] == 'ir.ui.menu'):
            new_ids = [data['form']['chart_account_id']]
            objects = self.pool.get('account.account').browse(self.cr, self.uid, new_ids)
        return super(general_ledger, self).set_context(objects, data, new_ids, report_type=report_type)

    def __init__(self, cr, uid, name, context=None):
        super(transtech_atm_info_invoice_purpose, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time, 
            'lines':self.lines,
            #'show_discount':self._show_discount,
        })
report_sxw.report_sxw('report.atm.info.invoice.purpose', 'atm.info', 'addons/transtech_module/report/atm_info_invoice_purpose.rml', parser=transtech_atm_info_invoice_purpose, header='internal')
#report_sxw.report_sxw('report.account.general.ledger_landscape', 'account.account', 'addons/account/report/account_general_ledger_landscape.rml', parser=general_ledger, header='internal landscape')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
