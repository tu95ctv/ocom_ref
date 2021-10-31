from collections import defaultdict
from lru import lru
lru.clear()
import time
# lru = {}
# from seleniumwire.webdriver.support.ui import WebDriverWait
import time
from seleniumwire import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
driver = webdriver.Firefox(firefox_binary=binary)
u = main_u =  'https://dathangsi.vn/'
def get_u():
    global driver
    global u
    start = time.time()
    driver.get(u)
    end = time.time()
    print('time',end - start)
get_u()


driver.find_elements_by_id('username')[0].send_keys('ndt')
driver.find_elements_by_id('password')[0].send_keys('1')
driver.find_elements_by_id('username')[0]

driver.find_elements_by_xpath("//input[@class='lin_dangky']")[0].click()
u = 'https://dathangsi.vn/7153-khau-trang-bang-voan-che-co-da-nang.html'
get_u()
driver.find_elements_by_xpath("//input[@class='detail_ecom_cart']")[0].click()

u = 'https://dathangsi.vn/5436-dai-giu-ao-so-mi-.html'

get_u()
driver.find_elements_by_xpath("//input[@class='detail_ecom_cart']")[0].click()

