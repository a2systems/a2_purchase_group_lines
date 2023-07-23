from odoo import tools, models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date,datetime
from odoo.tools.safe_eval import safe_eval

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    group_line_ids = fields.One2many(comodel_name='purchase.order.group.lines',inverse_name='order_id')

class PurchaseOrderGroupLines(models.Model):
    _name = "purchase.order.group.lines"
    _description = "Purchase Order Group Lines"
    _auto = False

    order_id = fields.Many2one('purchase.order','Purchase Order')
    product_id = fields.Many2one('product.product','Producto')
    product_uom = fields.Many2one('product.product','Producto')
    product_qty = fields.Float('Cantidad')
    price_unit = fields.Float('Ptice Unit')
    price_subtotal = fields.Float('Price Subtotal')
    price_total = fields.Float('Price Total')

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        query = """
            select order_id,product_id,product_uom,max(id) as id, sum(product_qty) as product_qty,
            avg(price_unit) as price_unit, sum(price_subtotal) as price_subtotal, sum(price_total) as price_total
            from purchase_order_line group by 1,2,3
            """
        self._cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, query))


