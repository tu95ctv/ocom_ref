import builtins
rs = {name: getattr(builtins, name) for name in dir(builtins)}
rs2 = rs['len'](range(10))
print (rs2)