import requests
from lxml import etree, html

# u = 'https://www.cpubenchmark.net/cpu_list.php'
# rs = requests.get(u, timeout=3,verify=False)

# f=open(r'C:\Users\nguye\Desktop\crawler\1.html','wb')
# f.write(rs.content)
# f.close()

f=open(r'C:\Users\nguye\Desktop\crawler\1.html','r')
page_source = f.read()
f.close()


# def get_xml_indirect_links(page_source):#New function
#         parser = html.HTMLParser(recover=True, encoding='utf-8')
#         page_source_etree = etree.fromstring(page_source, parser=parser)
#         res = page_source_etree.xpath(".//*[@onclick] | .//a[starts-with(@href,'javascript:')] | .//a[starts-with(@href,'js:')] ")
#         return res
def get_node_text(node):
    return ''.join(node.itertext())
def get_xml_indirect_links(page_source):#New function
        parser = html.HTMLParser(recover=True, encoding='utf-8')
        page_source_etree = etree.fromstring(page_source, parser=parser)
        res = page_source_etree.xpath(".//table[@id='cputable']//tr")
        return res


rs = get_xml_indirect_links(page_source)
# print (len(rs))
r1 = rs[4]
rs1 = r1.tail
xmlstr = etree.tostring(r1, encoding='unicode', method='html')
print(xmlstr)

# print (len(r1.xpath('.//td')))
count =0
for r1 in rs:
    try:
        xml_tds = r1.xpath('.//td')
        node = xml_tds[0]
        node2 = xml_tds[1]
        node3 = xml_tds[2]
        node4 = xml_tds[3]
        print( ' '.join((get_node_text(i) for i in xml_tds)))
        count +=1
    except:
        pass

print (count)