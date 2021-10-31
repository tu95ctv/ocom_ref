import xlwings as xw
wb = xw.Book()  # this will create a new workbook
path = r'C:\d4\sonix\a_duc_bidcrawler\bidcrawler\webbc\assets\cache\abc.xlsx'
# path = r'C:\d4\sonix\a_duc_bidcrawler\bidcrawler\webbc\assets\cache\0f3e6e4976504272aad431e307cf0870.xlsx'
# path = r'C:\d4\sonix\a_duc_bidcrawler\bidcrawler\webbc\assets\cache\0cfd0c60030d4a1f9855e8510961dec8.xlsx'

def xlwings_simple_read():
    wb = xw.Book(path)
    sheet = wb.sheets[0]
    rs = sheet.range('B6').value
    print (rs)
    # sheet.to_pdf()
# xlwings_simple_read()

# def read_xlrd(path):
#     import xlrd
#     xlrd.open_workbook( path )

# read_xlrd(path)


import pandas as pd
import xlwings as xw
from datetime import datetime


def _process_xlsx_pd(filename):
    wb = xw.Book(filename)
    sheet = wb.sheets[0]
    for sheet in wb.sheets:
        sheet_value = sheet.used_range.value
        df = pd.DataFrame(sheet_value)
        yield df
    wb.close()
    return df

def read_msexcel(path):
    try:
        content = ''
        dfs = _process_xlsx_pd(path)
        for count, df in enumerate(dfs):
            content += f'sheet {count+1}\n'
            for key, rows in df.iterrows():
                rows = rows.fillna('').values.tolist()
                rows_data_list= [str(i) for i in rows if i !=None]
                content += ' '.join(rows_data_list) + '\n'
        return True, content
    except Exception as err:
        logging.error(err)
        return False, None
content = read_msexcel(path)
