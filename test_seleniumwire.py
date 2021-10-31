
# from seleniumwire.webdriver.support.ui import WebDriverWait
import time
from seleniumwire import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
options = {
    'disable_capture': True  # Don't intercept/store any requests
}
options = {}
driver = webdriver.Firefox(firefox_binary=binary, seleniumwire_options=options)
u = 'https://www2.ebid.pref.fukui.jp/ebidPPIGPublish/EjPPIj'

u = 'https://www.e-procurement.metro.tokyo.jp/SrvPublish?page=3&act=6'

u = 'https://www.chotatsu.e-aichi.jp/ebidPPIPublish/EjPPIj'


def interceptor(request):
    r = request
    # print('interceptor request', request.url)
    f = open(r'C:\Users\nguye\Desktop\crawler\2.html', 'r', encoding="utf-8")
    rs = f.read()   
    # print ('**request.response**', request.response)
    if request.response:
        print(
            request.url,
            request.response.status_code,
            request.response.headers['Content-Type']
        )
    print (r.url)
    # print (r.url, r.url == 'https://www.chotatsu.e-aichi.jp/ebidPPIPublish/EjPPIj')
    if r.url == 'https://www.chotatsu.e-aichi.jp/ebidPPIPublish/EjPPIj' or 1:
        print ('Yes')
        request.abort()
        request.create_response(
            status_code=200,
            headers={'Content-Type': 'text/html'},  # Optional headers dictionary
            body=rs # Optional body
        )
    # if r.url != 'https://www.chotatsu.e-aichi.jp/ebidPPIPublish/EjPPIj':
    #     request.abort()  
driver.request_interceptor = interceptor

u = 'https://www.chotatsu.e-aichi.jp/ebidPPIPublish/EjPPIj'

driver.get(u)
u2 = 'https://www.e-procurement.metro.tokyo.jp/SrvPublish?page=3&act=6'
driver.get(u2)
driver.back()




