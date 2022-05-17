# import re
# p = 'C:\Projects\Ensure_Solution\Assistance\App_WebReferences\Web_ERP_WebService\Web_ERP_Assistant'
# rs =re.search(r'.+(\\.+)$',p)
# rs =re.search(r'(?:.(?!\\))+$',p)

# print (rs and rs.group(0))

s = "{'default_type': 'opportunity', 'default_user_id':uid}"

pos = s.find('{')
if pos != -1:
    s = s[:pos+1] + "'search_default_won_status_is_pending': 1, " + s[1:]

print (s)