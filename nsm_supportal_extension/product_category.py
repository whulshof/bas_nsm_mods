# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2016 Magnus www.magnus.nl w.hulshof@magnus.nl
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _

class product_category(osv.osv):
    _inherit = "product.category"

    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name'], context=context)
        res = []
        for record in reads:
            name = record['name']
            res.append((record['id'], name))
        return res

    def name_get_full(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name','parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1]+' / '+name
            res.append((record['id'], name))
        return res

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get_full(cr, uid, ids, context=context)
        return dict(res)

    def _supplier_category_search(self, cr, uid, obj, name, args,  context=None):
        if not args or not isinstance(args[0][2], (int, long)) or not args[0][2]:
            return [('id', '=', False)]  # maybe raise NotImplemented?
        user = self.pool['res.users'].browse(cr, uid, args[0][2], context=context)
        supplier = user.partner_id  # partner_id is required on users
        if not supplier.product_category_ids:
            return [('id', '=', False)]
        cat_ids = [cat.id for cat in supplier.product_category_ids]
        portal_category_ids = self.search(cr, uid, [('supportal', '=', True)], context=context)
        portal_category_ids.extend(cat_ids)
        return [('id', 'in', portal_category_ids)]


    _columns = {
        'complete_name': fields.function(_name_get_fnc, type="char", string='Name'),
        'supportal': fields.boolean('Parent Portal Productcategorieen',  help="Indicator that determines the role of this category as parent of supplier portal categories."),
        'supp_category_ids': fields.function(lambda self, cr, uid, ids, field_name, arg, context=None: dict.fromkeys(ids, True), fnct_search=_supplier_category_search, type='integer', method=True,),
    }





# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
