from collections import defaultdict
from lru import lru
lru.clear()
import time
# lru = {}
# from seleniumwire.webdriver.support.ui import WebDriverWait
import time
from seleniumwire import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# profile = webdriver.FirefoxProfile()
# profile.set_preference("browser.cache.disk.enable", False)
# profile.set_preference("browser.cache.memory.enable", False)
# profile.set_preference("browser.cache.offline.enable", False)
# profile.set_preference("network.http.use-cache", False)
# from selenium.webdriver.firefox.options import Options
# options = Options()
# options.add_argument("--headless")
binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
# options = {
#     'disable_capture': True  # Don't intercept/store any requests
# }
# options = {}


# driver = webdriver.Firefox(profile, firefox_binary=binary, seleniumwire_options=options)
# driver = webdriver.Firefox(profile, firefox_binary=binary, options=options)
driver = webdriver.Firefox(firefox_binary=binary)
count_in = 0
count_out = 0
count_in_dict = defaultdict(int)
def request_interceptor(request):
    global count_in, count_out, count_in_dict
    print('interceptor request', request.url)
    if request.url in lru:
        count_in_dict[request.url] +=1
        rs = lru[request.url]
        # print (type(rs))
        request.response =rs
        count_in +=1
        # request.create_response(
        #         status_code=200,
        #         body=rs.body, # Optional body
        #         headers=dict(rs.headers)
        #     )
    else:
        count_out += 1

def request_interceptor(request):
    global count_in, count_out, count_in_dict
    print('interceptor request', request.url)
    if request.url in lru:
        print ('*****akakakakkkkkkkkkkkkkkk(*****')
        count_in_dict[request.url] +=1
        rs = lru[request.url]
        # print (type(rs))
        request.response =rs
        count_in +=1
        # request.create_response(
        #         status_code=200,
        #         body=rs.body, # Optional body
        #         headers=dict(rs.headers)
        #     )
    else:
        count_out += 1

def request_interceptor(request):
    global count_in, count_out, count_in_dict
    # print('interceptor request', request.url)
    if request.url in lru:
        print ('*****akakakakkkkkkkkkkkkkkk(*****')
        count_in_dict[request.url] +=1
        rs = lru[request.url]
        count_in +=1
        request.create_response(
                status_code=200,
                body=rs.body, # Optional body
                headers=dict(rs.headers)
            )
    else:
        count_out += 1


# def request_interceptor(rq):
#     print('interceptor request', rq.url)
#     pass


        
        
u = 'https://www.e-procurement.metro.tokyo.jp/index.jsp'
u='https://www.kagoshima-nyusatsu.jp/ebidPPIGPublish/EjPPIj'
u='https://www.jeed.go.jp/jeed/information/honbu/index.html'
u='https://e.vnexpress.net/'
u='https://www.jeed.go.jp/jeed/information/honbu/index.html'
u='https://www2.ebid.pref.fukui.jp/ebidPPIPublish/EjPPIj'
u='https://www.aist.go.jp/'
u = 'https://dantri.com.vn/'
u='https://edition.cnn.com/'
u='https://www.dailymail.co.uk/home/index.html'
u='https://www2.ppi.pref.hyogo.jp/ebidPPIPublish/EjPPIj'
#2
def response_interceptor(r,res):
    global u
    # print('interceptor ressponse', type(res))
    if r.url not in lru and r.url== u:
        print ('r.url== u')
        lru[r.url] = res







# u = 'https://www.e-procurement.metro.tokyo.jp/SrvPublish?page=3&act=6'
# driver.get(u)

# u = 'https://vnexpress.net'
# u = 'https://www.e-procurement.metro.tokyo.jp/SrvPublish?page=3&act=6'

#3
driver.request_interceptor = request_interceptor
driver.response_interceptor = response_interceptor
# u = 'https://www.e-procurement.metro.tokyo.jp/index.jsp'
# u='https://www.24h.com.vn/'
# u='https://vnexpress.net/'




def get_u():
    global driver
    global u
    start = time.time()
    driver.get(u)
    end = time.time()
    print('time',end - start)

    

get_u()

# driver.get(u)

# eles = driver.fin
# d_elements_by_xpath('//*[@onclick]')
# print (eles)
# eles[1].click()
# len(lru)
count_in
count_out
# count_in_dict


# driver.get("chrome://settings/clearBrowserData")
# profile = driver.FirefoxProfile()


# cache = driver.application_cache

lru.d.keys()
