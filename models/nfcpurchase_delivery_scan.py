from odoo import fields, models, api, _


class DeliveryScan(models.Model):
    _name = "nfcpurchase.delivery.scan"
    _description = "NfcPurchase Delivery Scan"

    delivery_order_uniq_id = fields.Char(string='Delivery Order Uniq Id', size=36, index=True)

    barcode = fields.Char(string="Barcode")
    qty = fields.Float(string="Quantity")

    def compute_get_delivery_order_uniq_id(self):
        model_delivery_scan = self.env["nfcpurchase.delivery.scan"]
        order_lines = self.env["nfcpurchase.purchase.order.line"].search([("barcode", "=", self.barcode)],
                                                                         order="create_date asc")
        if order_lines:
            for line in order_lines:
                delivery_scans = model_delivery_scan.search([
                    ("barcode", "=", self.barcode),
                    ("delivery_order_uniq_id", "=", line.delivery_order_uniq_id)
                ])
                if delivery_scans:
                    continue
                else:
                    self.delivery_order_uniq_id = line.delivery_order_uniq_id
