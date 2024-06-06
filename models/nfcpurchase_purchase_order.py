from odoo import fields, models, api, _


class PurchaseOrder(models.Model):
    _name = "nfcpurchase.purchase.order"
    _description = "NfcPurchase Purchase Order"

    uniq_id = fields.Char(string='Unique ID', size=36, required=True, index=True)
    change_id = fields.Char(string='Change ID', index=True)

    name = fields.Char(string="Name")
    receipt_number = fields.Char(string="Receipt Number")
    farmer_id = fields.Integer(string="Farmer")
    payment_id = fields.Integer(string="Payment")
    status = fields.Char(string="Status")
    purchase_event_id = fields.Integer(string="Purchase Event ID")
    is_paid = fields.Boolean(string="Paid")
    signature = fields.Binary(string="Signature")
    filename = fields.Char(default="image.png")
