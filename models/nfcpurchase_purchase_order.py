from odoo import fields, models, api, _


class PurchaseOrder(models.Model):
    _name = "nfcpurchase.purchase.order"
    _description = "NfcPurchase Purchase Order"

    uniq_id = fields.Char(string='Unique ID', size=36, required=True, index=True)
    change_id = fields.Char(string='Change ID', index=True)

    name = fields.Char(string="Name")
    receipt_number = fields.Char(string="Receipt Number")
    farmer_id = fields.Integer()
    farmer_odoo_true_id = fields.Many2one("nfcapp.farmer")
    payment_id = fields.Integer(string="Payment")
    status = fields.Char(string="Status")
    purchase_event_id = fields.Integer(string="Purchase Event ID")
    purchase_event_uniq_id = fields.Char()
    is_paid = fields.Boolean(string="Paid", compute="compute_is_paid")
    signature = fields.Binary(string="Signature")
    filename = fields.Char(default="image.png")
    date = fields.Date(string="Date")

    def compute_is_paid(self):
        money_entries = self.env["nfcpurchase.money"].search([
            ("purchase_order_uniq_id", "=", self.uniq_id)
        ])
        purchase_order_lines = self.env["nfcpurchase.purchase.order.line"].search([
            ("purchase_order_uniq_id", "=", self.uniq_id)
        ])

        total_payment = sum(money.amount for money in money_entries)
        grand_total = sum(line.subtotal for line in purchase_order_lines)
        calculation = total_payment + grand_total
        payment_positive = abs(total_payment)

        if payment_positive >= grand_total and int(total_payment) != 0:
            self.is_paid = True
        elif int(calculation) > 0:
            self.is_paid = False
        else:
            self.is_paid = False
