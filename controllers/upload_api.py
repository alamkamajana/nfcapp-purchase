import json
from odoo import http, tools
import json
import random
from werkzeug.utils import redirect
from odoo import http
from odoo.http import request, Response


MAPPED_FLASK_ODOO_MODEL = {
    "PurchaseEvent": "nfcpurchase.purchase.event",
    "PurchaseOrder": "nfcpurchase.purchase.order",
    "PurchaseOrderLine": "nfcpurchase.purchase.order.line",
    "Payment": "nfcpurchase.payment",
    "DeliveryOrder": "nfcpurchase.delivery.order",
    "Money": "nfcpurchase.money",
}


class nfcappPurchaseNewUploadApi(http.Controller):
    def _check_nfcapp_user_authentication(self, user_token):
        try:
            if user_token:
                if user_token == "nfcapp-AQ5cZefGuHSlMSMw":
                    return True
                else:
                    check_token = request.env['nfcapp.user'].sudo().search([('user_token','=',user_token)])
                    if check_token:
                        return True
                    else:
                        return False
            else:
                return False
        except:
            return False


    @http.route("/nfcpurchase/upload/all/get_ids/", methods=["POST"], cors="*", auth="public", csrf=False, type="json")
    def upload_all_get_ids(self, **params):
        json_data = request.jsonrequest
        token = json_data.get("token")
        if not token or not self._check_nfcapp_user_authentication(token):
            return json.dumps({"message": "Unauthorized", "status": 401})

        model = json_data.get("model")
        odoo_model_name = MAPPED_FLASK_ODOO_MODEL.get(model)
        if not odoo_model_name:
            return json.dumps({"message": "Invalid model", "status": 400})

        odoo_model = request.env[odoo_model_name]
        uniq_ids_to_create = []
        uniq_ids_to_update = []
        nfcpurchase_dict = json_data["nfcpurchase_dict"]

        for record in nfcpurchase_dict:
            uniq_id = record["uniq_id"]
            change_id = record["change_id"]
            check_data = odoo_model.sudo().search([("uniq_id", "=", uniq_id)], limit=1)
            if check_data:
                if change_id != check_data.change_id:
                    uniq_ids_to_update.append(uniq_id)
            else:
                uniq_ids_to_create.append(uniq_id)

        return_values = {
            "model": model,
            "to_create_list": uniq_ids_to_create,
            "to_update_list": uniq_ids_to_update
        }
        return json.dumps(return_values)


    @http.route("/nfcpurchase/upload/all/create/", methods=["POST"], cors="*", auth="public", csrf=False, type="json")
    def nfcpurchase_upload_all_create(self, **params):
        return self._process_upload_all("create")


    @http.route("/nfcpurchase/upload/all/update/", methods=["POST"], cors="*", auth="public", csrf=False, type="json")
    def nfcpurchase_upload_all_update(self, **params):
        return self._process_upload_all("update")


    def _process_upload_all(self, action):
        json_data = request.jsonrequest
        token = json_data.get("token")
        if not token or not self._check_nfcapp_user_authentication(token):
            return {"message": "Unauthorized", "status": 401}

        model = json_data.get("model")
        odoo_model_name = MAPPED_FLASK_ODOO_MODEL.get(model)
        if not odoo_model_name:
            return {"message": "Invalid model", "status": 400}

        odoo_model = request.env[odoo_model_name]
        upload_data = json_data.get("data")

        valid_fields = set(odoo_model.fields_get().keys())
        excluded_fields = ["id", "created", "modified", "create_uid", "write_uid"]
        filtered_upload_data = [{
            key: value
            for key, value in data.items()
            if key in valid_fields and key not in excluded_fields
        } for data in upload_data]

        for data in filtered_upload_data:
            if action == "create":
                odoo_model.sudo().create(data)
            elif action == "update":
                uniq_id = data.get("uniq_id")
                record = odoo_model.sudo().search([("uniq_id", "=", uniq_id)], limit=1)
                if record:
                    record.sudo().write(data)

        response = {"message": "Update success", "status": 200}
        return response


    @http.route("/nfcpurchase/upload/check_update/", type="json", methods=["POST"], cors="*", auth="public", csrf=False)
    def upload_check_update(self, **params):
        try:
            json_data = request.jsonrequest
            token = json_data.get("token")
            if not token or not self._check_nfcapp_user_authentication(token):
                return {"message": "Unauthorized", "status": 401}

            model = json_data.get("model")
            odoo_model_name = MAPPED_FLASK_ODOO_MODEL.get(model)
            if not odoo_model_name:
                return {"message": "Invalid model", "status": 400}

            odoo_model = request.env[odoo_model_name]
            uniq_id = json_data["uniq_id"]
            change_id = json_data["change_id"]

            find_uniq_id = odoo_model.sudo().search([("uniq_id", "=", uniq_id)], limit=1)
            if find_uniq_id:
                if find_uniq_id.change_id != change_id:
                    return {"model": model, "uniq_id": uniq_id, "update_type": "update"}
                else:
                    return {"model": model, "uniq_id": uniq_id, "update_type": False}
            else:
                return {"model": model, "uniq_id": uniq_id, "update_type": "create"}
        except Exception as e:
            return e

