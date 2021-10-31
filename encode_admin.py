import base64
# username, password = \
#             base64.b64decode(auth_data).decode("utf-8").split(":")
ad = 'admin:Jz8#fk(Vi'
ad = 'admin:admin'
rs = base64.b64encode(ad.encode("utf-8"))
print (rs)