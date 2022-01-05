# import pandas as pd
# import numpy as np
# FIELDS_BEFORE = ['a','b']
# FIELDS_AFTER = ['d','e']
# data = [[1,2],[3,4]]
# df = pd.DataFrame(data, columns=FIELDS_BEFORE, dtype=object)
# df['d'] = df['a'] + 10
# df['e'] = df['b'] 

# df = df[FIELDS_AFTER]
# rs = df.itertuples(index=False, name=None)
# print (rs)

# for  i in rs:
#     print (i)

def f():
    return {1:2}

for k,v in f.items():
    print (k,v)