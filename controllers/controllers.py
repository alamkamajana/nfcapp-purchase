import json
from odoo import http, tools
import json
import random
from werkzeug.utils import redirect
from odoo import http
from odoo.http import request, Response


class Controller(http.Controller):
    def compute_grand_total(self, po):
        po_lines = request.env["nfcpurchase.purchase.order.line"].search([
            ("purchase_order_uniq_id", "=", po.uniq_id)
        ])
        grand_total = sum(line.subtotal for line in po_lines)
        return grand_total

    @http.route("/nfcpurchase/view/purchase-event/<int:po_id>", auth="user", type="http", website=True)
    def view_purchase_event(self, po_id, **kw):
        if kw.get("pe_id"):
            pe_id = int(kw.get("pe_id"))
            purchase_event = request.env["nfcpurchase.purchase.event"].browse(pe_id)
            pe_uniq_id = purchase_event.uniq_id
            purchase_orders = request.env["nfcpurchase.purchase.order"].search([
                ("purchase_event_uniq_id", "=", pe_uniq_id)
            ])

            return_values = {
                "purchase_orders": purchase_orders,
                "purchase_event": purchase_event,
                "compute_grand_total": self.compute_grand_total,
                "po_odoo": purchase_event.purchase_order_odoo_true_id,
            }
            return request.render("nfcapp-purchase.web_nfcpurchase_purchase_event", return_values)

        purchase_events = request.env["nfcpurchase.purchase.event"].search([
            ("purchase_order_odoo_true_id", "=", po_id)
        ])
        po_odoo = request.env["purchase.order"].browse(po_id)

        def get_money_entries(pe_uniq_id):
            print("asdf")
            money_entries = request.env["nfcpurchase.money"].search([
                ("purchase_event_uniq_id", "=", pe_uniq_id)
            ])
            return money_entries

        def compute_money_in(pe_uniq_id):
            money_entries = get_money_entries(pe_uniq_id)
            money_out = sum(money.amount for money in money_entries if money.amount < 0)
            return money_out

        def compute_money_out(pe_uniq_id):
            money_entries = get_money_entries(pe_uniq_id)
            money_in = sum(money.amount for money in money_entries if money.amount > 0)
            return money_in

        def compute_balance(pe_uniq_id):
            money_entries = get_money_entries(pe_uniq_id)
            total_fund = sum(money.amount for money in money_entries)
            return total_fund

        def get_purchase_orders(pe_uniq_id):
            purchase_orders = request.env["nfcpurchase.purchase.order"].search([
                ("purchase_event_uniq_id", "=", pe_uniq_id)
            ])
            return purchase_orders

        return_values = {
            "purchase_events": purchase_events,
            "po_odoo": po_odoo,
            "compute_money_in": compute_money_in,
            "compute_money_out": compute_money_out,
            "compute_balance": compute_balance,
            "get_purchase_orders": get_purchase_orders,
            "compute_grand_total": self.compute_grand_total,
            "get_money_entries": get_money_entries,
        }
        return request.render("nfcapp-purchase.web_nfcpurchase_purchase_event", return_values)


    @http.route("/nfcpurchase/view/purchase-order/<int:po_id>", auth="user", type="http", website=True)
    def purchase_order_view(self, po_id, **kw):
        cashier = kw.get("cashier", None)
        purchase_order = request.env["nfcpurchase.purchase.order"].browse(po_id)
        purchase_event = request.env["nfcpurchase.purchase.event"].search([
            ("uniq_id", "=", purchase_order.purchase_event_uniq_id)
        ], limit=1)
        purchase_order_lines = request.env["nfcpurchase.purchase.order.line"].search([
            ("purchase_order_uniq_id", "=", purchase_order.uniq_id)
        ])
        money_entries = request.env["nfcpurchase.money"].search([
            ("purchase_order_uniq_id", "=", purchase_order.uniq_id)
        ])
        return_values = {
            "po_odoo": purchase_event.purchase_order_odoo_true_id,
            "purchase_order": purchase_order,
            "purchase_event": purchase_event,
            "purchase_order_lines": purchase_order_lines,
            "money_entries": money_entries,
            "cashier": cashier,
        }

        return request.render("nfcapp-purchase.web_nfcpurchase_purchase_order", return_values)


    @http.route("/nfcpurchase/view/delivery-order/<int:pe_id>", auth="user", type="http", website=True)
    def delivery_order_view(self, pe_id, **kw):
        purchase_event = request.env["nfcpurchase.purchase.event"].browse(pe_id)
        purchase_orders = request.env["nfcpurchase.purchase.order"].search([
            ("purchase_event_uniq_id", "=", purchase_event.uniq_id)
        ])
        purchase_order_lines = request.env["nfcpurchase.purchase.order.line"].search([
            ("purchase_order_uniq_id", "in", purchase_orders.mapped("uniq_id"))
        ])
        delivery_orders = request.env["nfcpurchase.delivery.order"].search([
            ("uniq_id", "in", purchase_order_lines.mapped("delivery_order_uniq_id"))
        ])

        def get_order_lines(delivery_uniq_id):
            order_lines = request.env["nfcpurchase.purchase.order.line"].search([
                ("delivery_order_uniq_id", "=", delivery_uniq_id)
            ])
            return order_lines

        def get_purchase_order(po_uniq_id):
            purchase_order = request.env["nfcpurchase.purchase.order"].search([
                ("uniq_id", "=", po_uniq_id)
            ], limit=1)
            return purchase_order

        return_values = {
            "purchase_event": purchase_event,
            "delivery_orders": delivery_orders,
            "get_order_lines": get_order_lines,
            "get_purchase_order": get_purchase_order,
        }

        return request.render("nfcapp-purchase.web_nfcpurchase_delivery_order", return_values)

