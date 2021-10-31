
input = '''AXCC 1 BuildingB 100 200
FEFS 1 BuildingB 300 400
FKJO 2 BuildingC 300 400
QPRO 2 BuildingB 150 200
QWER 1 BuildingC 500 600
GHRI 2 BuildingA 100 200
GJKK 2 BuildingC 500 700'''
input1='''SZJC 1 CharitySpire 124 190
ZMRO 1 CharitySpire 198 246
ATGL 1 CharitySpire 381 428
TUMA 1 CharitySpire 49 122
RJKV 1 CharitySpire 433 481
KBEL 1 CharitySpire 254 373'''
input2 = '''DZQG 2 CharitySpire 457 569
OMNL 1 CharitySpire 380 390
WXOJ 2 CharitySpire 279 448
FPCQ 1 CharitySpire 199 373
WGTU 2 CharitySpire 27 152
SOBH 2 CharitySpire 572 593
LLHH 1 CharitySpire 381 544
NADM 2 CharitySpire 162 272'''

input3 = '''BUJM 1 CharitySpire 179 200
STGD 2 CharitySpire 196 369
LSDP 2 CharitySpire 374 534
NCJV 1 CharitySpire 206 322
JFOM 1 CharitySpire 119 170
YQNN 3 CharitySpire 86 191
JDRC 3 CharitySpire 49 85
IVRC 3 CharitySpire 339 465
YFXX 3 CharitySpire 333 392
KFOV 3 CharitySpire 199 328
FGIG 1 CharitySpire 327 347
YGFL 2 CharitySpire 544 735'''

from collections import defaultdict
MOVE_TIME_LISTS = [['BuildingA', 'BuildingB', 150],
    ['BuildingA', 'BuildingC', 200],
    ['BuildingB', 'BuildingC', 100]]

def get_time_move(x,y):
    if x!=y:
        for MT in MOVE_TIME_LISTS:
            if x in MT and y in MT:
                return MT[-1]
    return 0

def convert(l):
    return l[0],int(l[1]),l[2], int(l[3]),int(l[4])

def main_(input):
    inputs = input.split('\n')
    inputs = [convert(x.split(' ')) for x in inputs if len(x)>2]
    groups = defaultdict(list)
    for i in inputs:
        groups[i[1]].append(i)
    for k in groups:
        groups[k] = sorted(groups[k], key= lambda i:(i[3],i[4]))
    
    invalid_res = defaultdict(list)
    for k in groups:
        for count,i in enumerate(groups[k]):
            check_in = i[3]  
            check_out = i[4] 
            bd = i[2]
            if count:
                move_time = get_time_move(bd0, bd)
                if check_in < check_out0 + move_time:
                    invalid_res[k].append(i)
                    continue
            bd0=bd
            check_out0 = check_out
    res = []
    for vals in invalid_res.values():
        for j in vals:
            res.append(j[0])
    res = sorted(res)
    res = ','.join(res)
    return res

res = main_(input)
print (res)
assert res=='FKJO,QPRO','Fail'
res = main_(input1)
assert res=='','Fail'
res = main_(input2)
assert res=='LLHH','Fail'
res = main_(input3)
assert res=='IVRC','Fail'


