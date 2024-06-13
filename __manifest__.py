{
    "name": "Nfcapp New Purchase",

    "summary": """
        New Purchase Applications For SAD""",

    "tag": """
        nfcapp
    """,

    "author": "ALAM",
    "website": "https://www.alamkamajana.com",

    "category": "sad",
    "version": "1",

    # any module necessary for this one to work correctly
    "depends": ["base", "hr", "nfcapp", "purchase"],

    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/nfcpurchase_views.xml",
        "views/nfcpurchase_purchase_order.xml",
        "views/nfcpurchase_purchase_order_line.xml",
        "views/nfcpurchase_payment.xml",
        "views/nfcpurchase_delivery_order.xml",
        "views/nfcpurchase_money.xml",
        "views/web_nfcpurchase_purchase_event.xml",
        "views/web_nfcpurchase_purchase_order.xml",
        "views/web_nfcpurchase_delivery_order.xml",
    ],

}
