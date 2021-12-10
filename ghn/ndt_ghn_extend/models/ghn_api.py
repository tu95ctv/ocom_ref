# -*- coding: utf-8 -*-
import requests
from odoo.exceptions import UserError
shop_id_87 = 1295159
token_87 = '81f253e7-e8da-11ea-84a7-3e05d9a3136e'
token_090 = '7e079abb-fe1d-11ea-aeaa-9a0707cfe569'
# token = token_87
shop_id_090 = 1318075 
# shop_id = shop_id_87
token = token_090#token_87
shop_id = shop_id_090#shop_id_87

token = token_87
shop_id = shop_id_87
otp = '783122'
ghn_config = {'token': token, 'shop_id':shop_id_87}


# def fetch_ghn(url,  data=None ,more_headers ={}, ghn_config={}):
#     token = ghn_config.get('token')
#     if not token:
#         raise UserError('Bạn phải nhập token ở setting')
#     headers = {'token': token }
#     headers.update(more_headers)
#     response = requests.post(url, 
#                              headers=headers, json =  data)
#     json_response = response.json()
#     return json_response

def fetch_2_ghn(url, token, shop_id=None, data=None):
    if not token:
        raise UserError('Bạn phải nhập token ở setting')
    headers = {'token': token }
    if shop_id:
        headers.update({'shop_id':str(shop_id)})
    response = requests.post(url, 
                             headers=headers, json =  data)
    json_response = response.json()
    return json_response

def fetch_3_ghn(url, token, shop_id=None, data=None):
    json_response = fetch_2_ghn(url, token, shop_id, data)
    print ('**trả về của ghn***', json_response)
    code  = json_response['code']
    if code == 200:
        return json_response['data']
    else:
        raise UserError(json_response['message'])

def fetch_ghn_fee(token, shop_id, to_district_id, to_ward_code,service_type_id,service_id, from_district_id , 
    height=0, length=0, width=0, weight=0):
        url = 'https://online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/fee'
        # shop_id = int(ghn_config.get('shop_id'))
        if shop_id == False:
            raise UserError('Phải cấu hình GHN shop id trong kho hàng')
        # more_headers = {"shop_id":str(shop_id)}
        if not weight:
            # raise UserError('Trọng lượng phải lớn hơn 0')
            weight = 1
        print ('to_district_id',to_district_id)
        #1A0112
        data = {    
                    "service_type_id":service_type_id,
                    "to_district_id":to_district_id,
                    "to_ward_code":to_ward_code,# char
                    "height":height,
                    "length":length,
                    "width":width,
                    "weight":weight,
                    "coupon": None}
        # r = fetch_ghn(url, data, more_headers, ghn_config=ghn_config)
        rs = fetch_3_ghn(url, token, shop_id, data)
        return rs

def fetch_ghn_order(token, shop_id, to_district_id, to_ward_code, to_address,service_id,service_type_id,
    delivery_payment_type_id, delivery_cod_amount,note,to_name,to_phone,
    items,height=0, length=0, width=0, weight=0):
    # shop_id = ghn_config['shop_id']
    url = 'https://online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/create'
    # more_headers = {"ShopId": str(shop_id)}
    
    data ={
    "payment_type_id": delivery_payment_type_id,#selection, nếu thu hộ tiền thì onchage cái này lên 2 ( buyer)
    "note": note,
    "required_note": "KHONGCHOXEMHANG",
    "return_phone": "",
    "return_address": "",
    "return_district_id": None,
    "return_ward_code": "",
    "client_order_code": "",# SO name
    "to_name": to_name,#need change
    "to_phone": to_phone,#need change
    "to_address": to_address,
    "to_ward_code": to_ward_code,
    "to_district_id": to_district_id,
    "cod_amount": delivery_cod_amount,#phải thu hộ tiền, hay đã chuyển khoản
    "content": note,# Nội dung đơn hàng
    "weight": weight,
    "length": length,
    "width": width,
    "height": height,

    "pick_station_id": 0,
    "deliver_station_id": 0,
    # "insurance_value": 2000000,
    "service_id": service_id,# có thể chỉ cần service_type_id là đủ
    "service_type_id":service_type_id,

    "items":items
    # [
    #     {
    #         "name":"quần dài",
    #         "code":"sip123",
    #         "quantity":1
    #     }
    # ]
}
    rt = fetch_3_ghn(url, token, shop_id, data)
    return rt
### mô hình affiliate ### chưa test thành công
# def addStafftoStore_by_OTP():
#     url = 'https://online-gateway.ghn.vn/shiip/public-api/v2/shop/affiliateCreateWithShop'
#     # url = 'https://dev-online-gateway.ghn.vn/shiip/public-api/v2/shop/affiliateCreateWithShop'
#     data = {
#         "phone": "0903884259",
#          "otp": otp, 
#          "shop_id": shop_id
#         }
#     r = fetch_ghn(url, data)
#     print ('trả về', r)
#     return r['data']

# def Create_Store_by_OTP():
#     url = 'https://online-gateway.ghn.vn/shiip/public-api/v2/shop/affiliateCreate'
#     data = {
#        "phone": "0903884259",
#         "otp": otp,
#         "address":"35 đồng đen",
#         "district_id":1442,
#         "ward_code":"20106"
#         }
#     r = fetch_ghn(url,  data)
#     print ('trả về', r)
#     return r['data']

# def get_OTP():
#     url = 'https://online-gateway.ghn.vn/shiip/public-api/v2/shop/affiliateOTP'
#     data = {
#        "phone": "0916022787",
#         }
#     r = fetch_ghn(url,  data)
#     print ('trả về', r)
#     rt =  r['data']
#     return rt

def get_ghn_order_info(token, ghn_order):
    url = 'https://online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/detail'
    data = {"order_code": ghn_order}
    rt = fetch_3_ghn(url,token,None, data)
    return rt

def cancel_ghn_shipment(token, ghn_order):
    # trả về: rt: data trả về
    url = 'https://online-gateway.ghn.vn/shiip/public-api/v2/switch-status/cancel'
    data = {"order_codes": ghn_order }
    rt = fetch_3_ghn(url,token,None,data)
    return rt

def ghn_update_order(token, ghn_order, data):
    url = 'https://online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/update'
    data.update({"order_code": ghn_order})
    rt = fetch_3_ghn(url,token,None,data)
    return rt
   
def get_fee_of_order(token, ghn_order):
    url = 'https://online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/soc'
    data = {"order_code": ghn_order}
    rt = fetch_3_ghn(url,token,None,data)
    return rt

def get_service(token, shop_id, from_district, to_district):
    url = 'https://online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/available-services'
    shop_id = int(ghn_config['shop_id'])
    if not shop_id:
        raise UserError('Phải cấu hình GHN shop id trong kho hàng')
    if not to_district:
        raise UserError('Bạn chưa set địa điểm đích để lấy dịch vụ ghn')
    if not from_district:
        raise UserError('Bạn chưa set địa nguồn để lấy dịch vụ ghn')
    data = {
    "shop_id": shop_id,#bắt buộc
	"from_district": from_district,#bắt buộc
	"to_district": to_district##bắt buộc
    }
    rt = fetch_3_ghn(url, token, None, data)
    return rt


if __name__ == "__main__":
    from_district =  3135
   