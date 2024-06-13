from odoo import fields, models, api, _


class PurchaseEvent(models.Model):
    _name = "nfcpurchase.purchase.event"
    _description = "NfcPurchase Purchase Event"

    uniq_id = fields.Char(string='Unique ID', size=36, required=True, index=True)
    change_id = fields.Char(string='Change ID', index=True)

    name = fields.Char(string='Name')
    fund = fields.Float(string='Fund')
    ics = fields.Char(string='ICS')
    purchaser_id = fields.Integer(string='Purchaser')
    cashier_id = fields.Integer(string='Cashier')
    ap_name = fields.Char(string='AP Name')
    ip_address = fields.Char(string='IP Address')
    purchase_order_odoo_id = fields.Integer(string='Purchase Order')
    purchase_order_odoo_true_id = fields.Many2one("purchase.order")
    note = fields.Text(string="Note")
    date_stamp = fields.Date(string='Date Stamp')

    def open_purchase_event(self):
        po_odoo_id = self.purchase_order_odoo_true_id.id
        pe_id = self.id
        link = f"/nfcpurchase/view/purchase-event/{po_odoo_id}?pe_id={pe_id}"
        return {
            'type': 'ir.actions.act_url',
            'url': link,
            'target': 'new',
        }
