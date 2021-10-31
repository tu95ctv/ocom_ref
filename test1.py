# l = []
# for i in range(2):
#     print (hex(id(l)))
#     l.append(i)
#     print (hex(id(l)))
#     print (l)

import os
path = r'C:\d4\sonix\a_duc_bidcrawler\bidcrawler\webbc\assets\cache'
list_of_files = {}
for (dirpath, dirnames, filenames) in os.walk(path):
    for filename in filenames:
        if 'git' not in filename:
	        list_of_files[filename] = os.sep.join([dirpath, filename])

print (list_of_files)

from core.utils import file_helpers
for path in list_of_files.values():
    print (path)
    ret, content = file_helpers.read_msexcel(path)
    print (bool(content))
    # print ('content', content)

import pandas as pd


def _process(filename):
  wb = xw.Book(filename)
  sheet = wb.sheets[0]
  df = sheet.used_range.options(pd.DataFrame, sheet_name=None,header=True).value
  wb.close()
  return df


import pandas as pd
import xlrd
for path in list_of_files.values():
    print (path)
    try:
        wb = xlrd.open_workbook( path )
        # df = pd.read_excel(path, sheet_name=None, header=None)
        # df = _process(path)
    except xlrd.biffh.XLRDError as e:# lỗi mật khẩu
        print ('lỗi mật khẩu: %s'%e)
        pass

path = 'C:\d4\sonix\a_duc_bidcrawler\bidcrawler\webbc\assets\cache\93268e6262a0480baa458304e6d5099a.xlsx'
path = r'C:\d4\sonix\a_duc_bidcrawler\bidcrawler\webbc\assets\cache\0cfd0c60030d4a1f9855e8510961dec8.xlsx'
# path = r'C:\d4\sonix\a_duc_bidcrawler\bidcrawler\webbc\assets\cache\abc.xlsx'
def _process(filename):
    import xlwings as xw
    wb = xw.Book(filename)
    sheet = wb.sheets[0]
    df = sheet.used_range.options(pd.DataFrame, sheet_name=None,header=True).value
    wb.close()
    return df
    
#đoạn code của anh Đức
from datetime import datetime
content = ''
df = pd.read_excel(path, sheet_name=None, header=None)
for key, value in df.items():
    data_list = value.fillna('').values.tolist()
    for row in data_list:
        for col in row:
            if isinstance(col, datetime):
                try:
                    row[row.index(col)] = col.strftime("%Y/%m/%d")
                except:
                    row[row.index(col)] = str(col)
            else:
                row[row.index(col)] = str(col)
        content += ' '.join(row) + '\n'


def _process(filename):
    import xlwings as xw
    wb = xw.Book(filename)
    sheet = wb.sheets[0]
    df = sheet.used_range.options(pd.DataFrame, sheet_name=None,header=True).value
    wb.close()
    return df
  
path = r'C:\d4\sonix\a_duc_bidcrawler\bidcrawler\webbc\assets\cache\0cfd0c60030d4a1f9855e8510961dec8.xlsx'
# df = pd.read_excel(path, sheet_name=None, header=None)
df = _process(path)
for key, value in df.items():
    print ('key',key)
    print ('value',value, 'type value', type(value))
    data_list = value.fillna('').values.tolist()
    print ('**data_list', data_list)
    # for row in data_list:
    #     for col in row:
            # print ('row',row, type(row))
            # row[row.index(col)] = str(col)
        # content += ' '.join(row) + '\n'







