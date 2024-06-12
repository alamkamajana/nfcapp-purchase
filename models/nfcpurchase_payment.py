from odoo import fields, models, api, _


class Payment(models.Model):
    _name = "nfcpurchase.payment"
    _description = "NfcPurchase Payment"

    uniq_id = fields.Char(string='Unique ID', size=36, required=True, index=True)
    change_id = fields.Char(string='Change ID', index=True)

    purchase_order_id = fields.Integer(string="Purchase Order")
    debit = fields.Float(string="Debit")
    credit = fields.Float(string="Credit")
    note = fields.Char(string="Note")
    purchase_event_id = fields.Integer(string="Purchase Event")
    purchase_event_uniq_id = fields.Char()
