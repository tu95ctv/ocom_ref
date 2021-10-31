import requests
from bs4 import BeautifulSoup
import re
import time
import subprocess
import pandas as pd


def reCheck(url):
    if 'https' in url:
        return url
    else:
        return url.replace('http','https')

def getFullURL(url_check):
    if '.html' in url_check:
        return  url_check.rsplit('/', 1)[0]
    elif '.htm' in url_check:
        return  url_check.rsplit('/', 1)[0]
    else:
        return  url_check

def getParentURL(full_url,root_url):
    # print(f'vv {full_url.split(root_url)[1]}')
    if full_url.split(root_url)[1] is None:
        return '/'
    else:
        if full_url.split(root_url)[1][-1] == '/':
            return  full_url.split(root_url)[1]
        else:
            return  full_url.split(root_url)[1]+'/'


def checkList(url_check,root_url):
    # url_check = 'https://www.city.adachi.tokyo.jp/noze/kurashi/zekin/kobai.html'
    parent_url=''
    full_url=''
    url_check = reCheck(url_check)
    # root_url ='city.adachi.tokyo.jp'
    
    full_url=  getFullURL(url_check)
    
    parent_url =  getParentURL(full_url,root_url)

    print(f'----------------------------------------')
    print(f'root {root_url}')
    print(f'full {full_url}')
    print(f'parent {parent_url}')
    print(f'----------------------------------------')

    source_code =  subprocess.check_output(f'curl -s  {url_check} ', shell=True,stderr=subprocess.STDOUT)
    # source_code =  subprocess.check_output(f'curl  {url_check}', shell=False,stderr=subprocess.STDOUT)
    
    # source_code = requests.get('https://www.city.adachi.tokyo.jp/noze/kurashi/zekin/kobai.html')
    soup = BeautifulSoup(source_code, 'html.parser')
    data = []
    links = []

    # print(f'soup {soup}')

    def remove_duplicates(l): # remove duplicates and unURL string
        for item in l:
            match = re.search("(?P<url>https?://[^\s]+)", item)
            if match is not None:
                links.append((match.group("url")))

    print(f'Process...')

    for link in soup.find_all('a', href=True):
        li = str(link.get('href'))
        # print(f'li {li}')
        if parent_url in li:
            print(f'link s {li}')
            data.append(li)
    
    for link in soup.find_all('div'):
        li = str(link.get('data-url'))
        if parent_url in li:
            print(f'data link s {li}')
            data.append(li)
    
    for link in soup.find_all('div'):
        li = str(link.get('data-href'))
        if parent_url in li:
            print(f'data href s {li}')
            data.append(li)
            
    # remove_duplicates(data)

    # for url in links:
    #     print(url)

    # Check total 
    total_check = len(data)

    # # Write file
    # write_process = pd.DataFrame([[total_check]], columns=["total"])
    # with pd.ExcelWriter("./links.xlsx",mode="a", engine="openpyxl") as writer:
    #     write_process.to_excel(writer)

    array_result_check.append(total_check)

    print(f'Done!! Total is: {total_check}')

#  Get data test from excel file
df = pd.read_excel(r'C:\d4\tu_code_odoo\ocom_ref\crawler\links_2.xlsx',index_col=None, na_values=['NA'], engine='openpyxl')

array_result_check=[]

def init():
    # Check each data from list test case
    for i in range(len(df.links)):
        # print(f'range {i}')
        checkList(df.links[i],df.root[i])

    print(f'Result: ')
    for i in range(len(array_result_check)):
        print(f'{df.links[i]}: {array_result_check[i]}')
# Run function
init()