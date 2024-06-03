from odoo import fields, models, api, _


class PurchaseOrderLine(models.Model):
    _name = "nfcpurchase.purchase.order.line"
    _description = "NfcPurchase Purchase Order Line"

    uniq_id = fields.Char(string='Unique ID', size=36, required=True, index=True)
    change_id = fields.Char(string='Change ID', index=True)

    product_odoo_id = fields.Integer(string="Product Odoo")
    qty = fields.Float(string="Quantity")
    unit_price = fields.Float(string="Unit Price")
    barcode = fields.Char(string="Barcode")
    subtotal = fields.Float(string="Subtotal")
    currency = fields.Char(string="Currency")
    delivery_order_id = fields.Integer(string="Delivery Order")
    purchase_order_id = fields.Integer(string="Purchase Order")
