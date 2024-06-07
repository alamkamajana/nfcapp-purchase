from odoo import fields, models, api, _


class DeliveryOrder(models.Model):
    _name = "nfcpurchase.delivery.order"
    _description = "NfcPurchase Delivery Order"

    uniq_id = fields.Char(string='Unique ID', size=36, required=True, index=True)
    change_id = fields.Char(string='Change ID', index=True)

    name = fields.Char(string="Name")
    driver = fields.Char(string="Driver")
    vehicle_number = fields.Char(string="Vehicle Number")
    purchase_event_id = fields.Integer(string="Purchase Event")
    sent_date = fields.Datetime()
    received_date = fields.Datetime()
    origin = fields.Char()
    destination = fields.Char(string="Destination")
    note = fields.Text(string="Note")
    status = fields.Char()
