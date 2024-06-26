import json
from odoo import http, tools
import json
import random
from werkzeug.utils import redirect
from odoo import http
from odoo.http import request, Response


class nfcappPurchaseNewApi(http.Controller):
    def _check_nfcap_user_authentication(self, token):
        try :
            if token :
                if token == "nfcapp-AQ5cZefGuHSlMSMw" :
                    return True
                else :
                    return False
            else :
                return False
        except :
            return False




    @http.route('/api/purchase/login', methods=['POST', 'OPTIONS'], type='json', cors="*", auth="none", csrf=False)
    def nfcapp_api_purchase_login(self, **params):
        try:
            data_json = json.loads(request.httprequest.data)
            username = data_json.get("username")
            password = data_json.get("password")
            database = data_json.get("database")
            request.session.authenticate(database, username, password)
            login_endpoint = request.env['ir.http'].sudo().session_info()
            user_id = login_endpoint.get("uid")
            session = request.session.get("session_token")

            nfcap_user = request.env['nfcapp.user'].sudo().search([('user_odoo', '=', int(user_id))])
            user_data = {}
            user_data['user_odoo_id'] = user_id
            user_data['token'] = session
            user_data['status'] = True
            user_data['message'] = 'success'
            user_data['name'] = nfcap_user.username
            user_data['fname'] = nfcap_user.first_name
            user_data['lname'] = nfcap_user.last_name
            user_data['email'] = nfcap_user.email
            user_data['phone'] = nfcap_user.phone
            user_station_arr = []
            user_station = nfcap_user.station

            if user_station:
                for stt in user_station:
                    station_dict = {
                        "id": stt.id,
                        "created": stt.create_date.strftime(
                            '%Y-%m-%d %H:%M:%S') if stt.create_date else None,
                        "modified": stt.write_date.strftime(
                            '%Y-%m-%d %H:%M:%S') if stt.write_date else None,
                        "name": stt.name,
                        "province": stt.province,
                        "gps_latitude": stt.gps_latitude,
                        "gps_longitude": stt.gps_longitude,
                        "is_testing": stt.is_testing
                    }
                    user_station_arr.append(station_dict)
            user_data['station'] = user_station_arr
            user_data['id'] = nfcap_user.id
            user_data['tipe'] = nfcap_user.tipe
            user_data['isSU'] = nfcap_user.is_superuser
            user_data['cluster'] = {}
            user_data['farmer'] = {}
            user_data['sssDate'] = None
            user_data['jsonrpc'] = '2.0'
            user_data['user_token'] = nfcap_user.user_token
            user_data['status'] = 200
            return user_data
        except Exception as e:
            print(e)
            return {
                "message" : "error", "status" : 400
            }
    @http.route('/nfcapp-purchase/get-product', csrf=False, cors="*", type='http', auth="none")
    def nfcapp_purchase_get_product(self, **params):
        try :
            token = params.get("token")
            odoo_user_id = params.get("odoo_user_id")
            nfcapp_check_access = self._check_nfcap_user_authentication(token)
            if not nfcapp_check_access:
                return False

            odoo_user = request.env['res.users'].sudo().browse(int(odoo_user_id))
            followers = request.env['mail.followers'].search([
                ('res_model', '=', 'purchase.order'),
                ('partner_id', '=', odoo_user.partner_id.id)
            ])
            product_po = []
            purchase_orders = request.env['purchase.order'].sudo().browse(followers.mapped('res_id'))
            po_arr = []
            for po in purchase_orders:
                po_arr.append(po.id)

            po_line_arr = []
            data_po_line = request.env['purchase.order.line'].sudo().search([('order_id', 'in', po_arr)])
            for po_line in data_po_line:
                if po_line.product_id :
                    product_po.append(po_line.product_id.id)
            product_ids = []
            commodity_product = request.env['nfcapp.commodityitem'].sudo().search([('product_id','!=',False)])
            for cmd in commodity_product:
                product_ids.append(cmd.product_id.id)
            product_ids2 = product_po + product_ids
            product_arr = []
            data_product  = request.env['product.product'].sudo().search([('id','in',product_ids2)])
            for product in data_product :
                product_json = {}
                product_json['id'] = product.id
                product_json['active'] = product.active
                product_json['barcode'] = product.barcode
                product_json['default_code'] = product.default_code
                product_json['product_tmpl_id'] = product.product_tmpl_id.id if product.product_tmpl_id else None
                product_json['name'] = product.name
                product_json['volume'] = product.volume
                product_json['weight'] = product.weight
                product_json['type'] = product.type
                product_json['item_code'] = product.itemcode
                product_json['commodity'] = product.commodity
                product_json['odoo_id'] = product.id
                product_json['write_date'] = product.write_date

                product_arr.append(product_json)

            result = json.dumps(product_arr,default=str, indent=4, sort_keys=True)
            response = Response(result, content_type='application/json;charset=utf-8', status=200)
            return response
        except Exception as e :
            print(e)
            return e

    @http.route('/nfcapp-purchase/get-purchase-order', csrf=False, cors="*", type='http', auth="none")
    def nfcapp_purchase_get_purchase_order(self, **params):
        try :
            token = params.get("token")
            odoo_user_id = params.get("odoo_user_id")
            nfcapp_check_access = self._check_nfcap_user_authentication(token)
            if not nfcapp_check_access:
                return False

            odoo_user = request.env['res.users'].sudo().browse(int(odoo_user_id))
            followers = request.env['mail.followers'].search([
                ('res_model', '=', 'purchase.order'),
                ('partner_id', '=', odoo_user.partner_id.id)
            ])
            # purchase_orders2 = request.env['purchase.order'].sudo().browse(followers.mapped('res_id'))
            purchase_orders = request.env['purchase.order'].sudo().search([('id','in',followers.mapped('res_id')),('incoterm_id','=',18)])
            po_arr = []
            for po in purchase_orders :
                po_json = {}
                po_json['id'] = po.id
                po_json['name'] = po.name
                po_json['access_token'] = po.access_token
                po_json['partner_id'] = po.partner_id.id if po.partner_id else None
                po_json['partner_name'] = po.partner_id.name if po.partner_id else None
                po_json['partner_ref'] = po.partner_ref
                po_json['analytic_account_id'] = po.analytic_account_id.id if po.analytic_account_id else None
                po_json['analytic_account_name'] = po.analytic_account_id.name if po.analytic_account_id else None
                po_json['manager_id'] = po.manager_id.id if po.manager_id else None
                po_json['manager_name'] = po.manager_id.name if po.manager_id else None
                po_json['currency_name'] = po.currency_id.name if po.currency_id else None
                po_json['date_approve'] = po.date_approve if po.date_approve else None
                po_json['picking_type_name'] = po.picking_type_id.name if po.picking_type_id else None
                po_json['incoterm_name'] = po.incoterm_id.name if po.incoterm_id else None
                po_json['user_name'] = po.user_id.name if po.user_id else None
                po_json['payment_term_name'] = po.payment_term_id.name if po.payment_term_id else None
                po_json['odoo_id'] = po.id
                po_json['write_date'] = po.write_date
                po_arr.append(po_json)

            result = json.dumps(po_arr, default=str, indent=4, sort_keys=True)
            response = Response(result, content_type='application/json;charset=utf-8', status=200)
            return response
        except Exception as e :
            print(e)
            return e

    @http.route('/nfcapp-purchase/get-purchase-order-line', csrf=False, cors="*", type='http', auth="none")
    def nfcapp_purchase_get_purchase_order_line(self, **params):
        try :
            token = params.get("token")
            odoo_user_id = params.get("odoo_user_id")
            nfcapp_check_access = self._check_nfcap_user_authentication(token)
            if not nfcapp_check_access:
                return False

            odoo_user = request.env['res.users'].sudo().browse(int(odoo_user_id))
            followers = request.env['mail.followers'].search([
                ('res_model', '=', 'purchase.order'),
                ('partner_id', '=', odoo_user.partner_id.id)
            ])
            purchase_orders = request.env['purchase.order'].sudo().search(
                [('id', 'in', followers.mapped('res_id')), ('incoterm_id', '=', 18)])
            po_arr = []
            for po in purchase_orders:
                po_arr.append(po.id)

            po_line_arr = []
            data_po_line  = request.env['purchase.order.line'].sudo().search([('order_id','in',po_arr)])
            for po_line in data_po_line :
                po_line_json = {}
                po_line_json['id'] = po_line.id
                po_line_json['name'] = po_line.name
                po_line_json['product_id'] = po_line.product_id.id if po_line.product_id else None
                po_line_json['product_name'] = po_line.product_id.name if po_line.product_id else None
                po_line_json['product_qty'] = po_line.product_qty
                po_line_json['price_unit'] = po_line.price_unit
                po_line_json['date_planned'] = po_line.date_planned if po_line.date_planned else None
                po_line_json['order_id'] = po_line.order_id.id if po_line.order_id else None
                po_line_json['order_name'] = po_line.order_id.name if po_line.order_id else None
                po_line_json['odoo_id'] = po_line.id
                po_line_json['write_date'] = po_line.write_date

                po_line_arr.append(po_line_json)

            result = json.dumps(po_line_arr, default=str, indent=4, sort_keys=True)
            response = Response(result, content_type='application/json;charset=utf-8', status=200)
            return response
        except Exception as e :
            print(e)
            return e

    @http.route('/nfcapp-purchase/get-nfcapp-farmer', csrf=False, cors="*", type='http', auth="none")
    def nfcapp_purchase_get_nfcapp_farmer(self, **params):
        try :
            token = params.get("token")
            nfcapp_check_access = self._check_nfcap_user_authentication(token)
            if not nfcapp_check_access:
                return False

            nfcapp_farmer_arr = []
            data_nfcapp_farmer = request.env['nfcapp.farmer'].sudo().search([], order="id asc")
            for farmer in data_nfcapp_farmer :
                nfcapp_farmer_json = {}
                nfcapp_farmer_json['id'] = farmer.id
                nfcapp_farmer_json['parent_id'] = farmer.parent_id.id if farmer.parent_id else None
                nfcapp_farmer_json['parent_name'] = farmer.parent_id.name if farmer.parent_id else None
                nfcapp_farmer_json['station_id'] = farmer.parent_id.station_id.id if farmer.parent_id.station_id else None
                nfcapp_farmer_json['station_name'] = farmer.parent_id.station_id.name if farmer.parent_id.station_id else None
                nfcapp_farmer_json['code'] = farmer.code
                nfcapp_farmer_json['farmer_name'] = farmer.farmer_name
                nfcapp_farmer_json['farmer_role'] = farmer.farmer_role
                nfcapp_farmer_json['registration_date'] = farmer.registration_date if farmer.registration_date else None
                nfcapp_farmer_json['contract_date'] = farmer.contract_date if farmer.contract_date else None
                nfcapp_farmer_json['gender'] = farmer.gender
                nfcapp_farmer_json['date_of_birth'] = farmer.date_of_birth if farmer.date_of_birth else None
                nfcapp_farmer_json['phone_number'] = farmer.phone_number
                nfcapp_farmer_json['active'] = farmer.active
                nfcapp_farmer_json['no_ktp'] = farmer.no_ktp
                nfcapp_farmer_json['bank_akun'] = farmer.bank_akun
                nfcapp_farmer_json['certification_status_id'] = farmer.certification_status_id.id
                nfcapp_farmer_json['certification_status_name'] = farmer.certification_status_id.name
                nfcapp_farmer_json['bank_holder'] = farmer.bank_holder
                nfcapp_farmer_json['bank_name_name'] = farmer.bank_name_id.name if farmer.bank_name_id else None
                nfcapp_farmer_json['odoo_id'] = farmer.id
                nfcapp_farmer_json['write_date'] = farmer.write_date

                commodity_arr = []
                data_commodity = request.env['nfcapp.commodityitem'].sudo().search([('certStatus','in',farmer.certification_status_id.id)])
                for commodity in data_commodity:
                    commodity_json = {}
                    commodity_json['farmer_id'] = farmer.id
                    commodity_json['id'] = commodity.id
                    commodity_json['code'] = commodity.code
                    commodity_json['desc'] = commodity.desc
                    commodity_json['price'] = commodity.price
                    commodity_json['commodity_id'] = commodity.commodity_id.id if commodity.commodity_id else None
                    commodity_json['commodity_name'] = commodity.commodity_id.name if commodity.commodity_id else None
                    commodity_json['variant'] = commodity.variant
                    commodity_json['packing'] = commodity.packing
                    commodity_json['product_id'] = commodity.product_id.id if commodity.product_id else None
                    commodity_json['product_id_code'] = commodity.product_id.itemcode if commodity.product_id else None
                    commodity_json['product_id_name'] = commodity.product_id.name if commodity.product_id else None
                    commodity_json['product_name'] = commodity.product_id.name if commodity.product_id else None
                    commodity_json['odoo_id'] = commodity.id
                    commodity_json['certStatus'] = str(commodity.certStatus.ids)
                    commodity_json['write_date'] = commodity.write_date

                    cert_ids = commodity.certStatus.mapped('certification_id')

                    total_premium=0
                    cu_number =""
                    for cert_id in cert_ids:
                        total_premium = cert_id.premium_purchase
                        if cert_id.no:
                            cu_number = cu_number+", "+cert_id.no


                    commodity_json['total_premium'] = commodity.total_premium
                    commodity_json['cu_number'] = cu_number



                    if True in commodity.certStatus.mapped('is_organic'):
                        is_organic = True
                    else:
                        is_organic = False


                    if True in commodity.certStatus.mapped('is_ra_cert'):
                        is_ra_cert = True
                    else:
                        is_ra_cert = False




                    commodity_json['is_organic'] = commodity.organic
                    commodity_json['is_ra_cert'] = is_ra_cert

                    commodity_json['color_hex'] = commodity.color_hex
                    commodity_json['color_name'] = commodity.color_name






                    commodity_arr.append(commodity_json)

                nfcapp_farmer_json['commodity_items'] = commodity_arr

                # print(nfcapp_farmer_json)
                nfcapp_farmer_arr.append(nfcapp_farmer_json)

            result = json.dumps(nfcapp_farmer_arr, default=str, indent=4, sort_keys=True)
            response = Response(result, content_type='application/json;charset=utf-8', status=200)
            return response
        except Exception as e :
            print(e)
            return e

    @http.route('/nfcapp-purchase/get-res-user', csrf=False, cors="*", type='http', auth="none")
    def nfcapp_purchase_get_res_user(self, **params):
        try :
            # token = params.get("token")
            # nfcapp_check_access = self._check_nfcap_user_authentication(token)
            # if not nfcapp_check_access:
            #     return False
            user_ids = []
            nfcapp_user = request.env['nfcapp.user'].sudo().search([('user_odoo','!=', False)])
            for usr in nfcapp_user :
                user_ids.append(usr.user_odoo.id)
            res_user_arr = []
            data_res_user = request.env['res.users'].sudo().search([('id','in',user_ids)])
            for user in data_res_user :
                res_user_json = {}
                res_user_json['id'] = user.id
                res_user_json['active'] = user.active
                res_user_json['name'] = user.name
                res_user_json['login'] = user.login
                res_user_json['company_id'] = user.company_id.id if user.company_id else None
                res_user_json['partner_id'] = user.partner_id.id if user.partner_id else None
                res_user_json['partner_name'] = user.partner_id.name if user.partner_id else None
                res_user_json['email'] = user.email
                res_user_json['employee_id'] = user.employee_id.id if user.employee_id else None
                res_user_json['employee_name'] = user.employee_id.name if user.employee_id else None
                res_user_json['odoo_id'] = user.id
                res_user_json['write_date'] = user.write_date

                res_user_arr.append(res_user_json)

            result = json.dumps(res_user_arr, default=str, indent=4, sort_keys=True)
            response = Response(result, content_type='application/json;charset=utf-8', status=200)
            return response
        except Exception as e :
            print(e)
            return e

    @http.route('/nfcapp-purchase/get-commodity', csrf=False, cors="*", type='http', auth="none")
    def nfcapp_purchase_get_commodity(self, **params):
        try:
            token = params.get("token")
            nfcapp_check_access = self._check_nfcap_user_authentication(token)
            if not nfcapp_check_access:
                return False

            commodity_arr = []
            data_commodity = request.env['nfcapp.commodity'].sudo().search([], order="id asc")
            for commodity in data_commodity:
                commodity_json = {}
                commodity_json['id'] = commodity.id
                commodity_json['name'] = commodity.name
                commodity_json['station_id'] = commodity.station_id.id if commodity.station_id else None
                commodity_json['station_name'] = commodity.station_id.name if commodity.station_id else None
                commodity_json['odoo_id'] = commodity.id
                commodity_json['write_date'] = commodity.write_date

                commodity_arr.append(commodity_json)

            result = json.dumps(commodity_arr, default=str, indent=4, sort_keys=True)
            response = Response(result, content_type='application/json;charset=utf-8', status=200)
            return response
        except Exception as e:
            print(e)
            return e

    @http.route('/nfcapp-purchase/get-commodityitem', csrf=False, cors="*", type='http', auth="none")
    def nfcapp_purchase_get_commodityitem(self, **params):
        try:
            token = params.get("token")
            nfcapp_check_access = self._check_nfcap_user_authentication(token)
            if not nfcapp_check_access:
                return False

            commodity_arr = []
            data_commodity = request.env['nfcapp.commodityitem'].sudo().search([], order="id asc")
            for commodity in data_commodity:
                commodity_json = {}
                commodity_json['id'] = commodity.id
                commodity_json['code'] = commodity.code
                commodity_json['price'] = commodity.price
                commodity_json['commodity_id'] = commodity.commodity_id.id if commodity.commodity_id else None
                commodity_json['commodity_name'] = commodity.commodity_id.name if commodity.commodity_id else None
                commodity_json['variant'] = commodity.variant
                commodity_json['packing'] = commodity.packing
                commodity_json['product_id'] = commodity.product_id.id if commodity.product_id else None
                commodity_json['product_name'] = commodity.product_id.name if commodity.product_id else None
                commodity_json['odoo_id'] = commodity.id
                commodity_json['write_date'] = commodity.write_date

                commodity_arr.append(commodity_json)

            result = json.dumps(commodity_arr, default=str, indent=4, sort_keys=True)
            response = Response(result, content_type='application/json;charset=utf-8', status=200)
            return response
        except Exception as e:
            print(e)
            return e

    @http.route('/nfcapp-purchase/get-station', csrf=False, cors="*", type='http', auth="none")
    def nfcapp_purchase_get_station(self, **params):
        try:
            token = params.get("token")
            nfcapp_check_access = self._check_nfcap_user_authentication(token)
            if not nfcapp_check_access:
                return False

            station_arr = []
            data_station = request.env['nfcapp.station'].sudo().search([], order="id asc")
            for station in data_station:
                station_json = {}
                station_json['id'] = station.id
                station_json['name'] = station.name
                station_json['province'] = station.province
                station_json['gps_latitude'] = station.gps_latitude
                station_json['gps_longitude'] = station.gps_longitude
                station_json['is_testing'] = station.is_testing
                station_json['odoo_id'] = station.id
                station_json['write_date'] = station.write_date

                station_arr.append(station_json)

            result = json.dumps(station_arr, default=str, indent=4, sort_keys=True)
            response = Response(result, content_type='application/json;charset=utf-8', status=200)
            return response
        except Exception as e:
            print(e)
            return e

    @http.route('/nfcapp-purchase/get-cluster', csrf=False, cors="*", type='http', auth="none")
    def nfcapp_purchase_get_cluster(self, **params):
        try:
            token = params.get("token")
            nfcapp_check_access = self._check_nfcap_user_authentication(token)
            if not nfcapp_check_access:
                return False

            cluster_arr = []
            data_cluster = request.env['nfcapp.cluster'].sudo().search([], order="id asc")
            for cluster in data_cluster:
                cluster_json = {}
                cluster_json['id'] = cluster.id
                cluster_json['name'] = cluster.name
                cluster_json['station_id'] = cluster.station_id.id if cluster.station_id else None
                cluster_json['station_name'] = cluster.station_id.name if cluster.station_id else None
                cluster_json['coordinator'] = cluster.coordinator
                cluster_json['code'] = cluster.code
                cluster_json['odoo_id'] = cluster.id
                cluster_json['write_date'] = cluster.write_date
                cluster_arr.append(cluster_json)

            result = json.dumps(cluster_arr, default=str, indent=4, sort_keys=True)
            response = Response(result, content_type='application/json;charset=utf-8', status=200)
            return response
        except Exception as e:
            print(e)
            return e

    @http.route('/nfcapp-purchase/sync-with-odoo', csrf=False, cors="*", type='http', auth="none")
    def nfcapp_purchase_sync_with_odoo(self, **params):
        try:
            token = params.get("token")
            nfcapp_check_access = self._check_nfcap_user_authentication(token)
            if not nfcapp_check_access:
                return False

            data_arr = []
            farmers = request.env['nfcapp.farmer'].sudo().search([('active','=',True)])
            for farmer in farmers :
                farmer_station = farmer.parent_id.station_id
                farmer_itemcode = request.env['nfcapp.commodityitem'].sudo().search([('commodity_id.station_id','=',farmer_station.id)])
                farmer_itemcode_arr = []
                farmer_product_arr = []
                for itemcode in farmer_itemcode :
                    farmer_itemcode_arr.append(itemcode.id)
                    if itemcode.product_id  :
                        farmer_product_arr.append(itemcode.product_id.id)

                farmer_dict = {}
                farmer_dict['odoo_id'] = farmer.id
                farmer_dict['farmer_name'] = farmer.farmer_name
                farmer_dict['farmer_code'] = farmer.code
                farmer_dict['item_code_list'] = farmer_itemcode_arr
                farmer_dict['product_list'] = farmer_product_arr
                data_arr.append(farmer_dict)

            result = json.dumps(data_arr)
            response = Response(result, content_type='application/json;charset=utf-8', status=200)
            return response
        except Exception as e:
            print(e)
            return e

