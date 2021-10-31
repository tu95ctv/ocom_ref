import os

def write(o,str_val=''):
    str_val = str(str_val)
    rt = 'fail'
    if str_val:
        full_path = o.env['ir.attachment']._filestore() 
        full_path = os.path.join(full_path, 'output.txt')
        bin_value = str_val.encode('utf-8')
        with open(full_path, 'wb') as fp:
            rt  = fp.write(bin_value)
    return rt

def read(o):
    full_path = o.env['ir.attachment']._filestore() 
    full_path = os.path.join(full_path, 'output.txt')
    with open(full_path, 'rb') as f:
        out= f.read()
    return out




