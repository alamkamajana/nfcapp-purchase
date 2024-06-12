from odoo import fields, models, api, _


class Money(models.Model):
    _name = "nfcpurchase.money"
    _description = "NfcPurchase Money"

    uniq_id = fields.Char(string='Unique ID', size=36, required=True, index=True)
    change_id = fields.Char(string='Change ID', index=True)

    number = fields.Char(string="Number")
    purchase_event_id = fields.Integer(string="Purchase Event")
    purchase_order_id = fields.Integer(string="Purchase Order")
    amount = fields.Float(string="Amount")
    note = fields.Text(string="Note")
    purchase_event_uniq_id = fields.Char()
    purchase_order_uniq_id = fields.Char()
