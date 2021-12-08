


import requests
def fetch_ghn(url, headers, data):
    response = requests.post(url, 
    headers=headers, json =  data)
    json_response = response.json()
    return json_response


def fetch_ghn_ward_data(ghn_district_id):
        headers = {'token': '81f253e7-e8da-11ea-84a7-3e05d9a3136e'}
        url = 'https://online-gateway.ghn.vn/shiip/public-api/master-data/ward?district_id'
        data = {"district_id": int(ghn_district_id)}#int(self.ghn_id)}
        r = fetch_ghn(url, headers, data)
        print (r)
        return r['data']
        
token = '81f253e7-e8da-11ea-84a7-3e05d9a3136e'
def ghn_province():
        headers = {'token': token}
        response = requests.post('https://online-gateway.ghn.vn/shiip/public-api/master-data/province', 
                headers=headers)
        rtj = response.json()
        ghn_provinces = rtj['data']
        print ('ghn_provinces',ghn_provinces)



# rs = fetch_ghn_ward_data(1)
rs = ghn_province()

print (rs)