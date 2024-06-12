from odoo import fields, models, api, _


class PurchaseOrderLine(models.Model):
    _name = "nfcpurchase.purchase.order.line"
    _description = "NfcPurchase Purchase Order Line"

    uniq_id = fields.Char(string='Unique ID', size=36, required=True, index=True)
    change_id = fields.Char(string='Change ID', index=True)

    product_odoo_id = fields.Integer(string="Product Odoo")
    product_odoo_true_id = fields.Many2one("product.product")
    nfcapp_commodity_item_odoo_id = fields.Integer()
    qty = fields.Float(string="Quantity")
    unit_price = fields.Float(string="Unit Price")
    barcode = fields.Char(string="Barcode")
    commodity_name = fields.Char(string="Commodity Name")
    variant = fields.Char(string="Variant")
    is_organic = fields.Boolean("Is Organic")
    is_ra_cert = fields.Boolean()
    color_name = fields.Char(string="Color Name")
    color_hex = fields.Char(string="Color HEX")
    subtotal = fields.Float(string="Subtotal")
    currency = fields.Char(string="Currency")
    delivery_order_id = fields.Integer(string="Delivery Order")
    purchase_order_id = fields.Integer(string="Purchase Order")
    note = fields.Text(string="Note")
    delivery_order_uniq_id = fields.Char()
    purchase_order_uniq_id = fields.Char()
