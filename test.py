

ck = 'PHPSESSID=pamumm0copph9clkc7n217mi00; cookie_favourite=pamumm0copph9clkc7n217mi00; _ga=GA1.2.1944990829.1635391972; cookie_district=15; _gid=GA1.2.55814734.1635565220; __zi=3000.SSZzejyD7Dy_WlYjp1OKdowViw-O25gHDjpllP8NIDCaolpyW505qI22jF-CN0JJP8gt_y5L0DPbWRpvCJW.1; cookie_namecity=1; cookie_firstname=Tứ+Nguyễn; cookie_address=13+Trương+Hoàng+Thanh; cookie_mobile=0916022787; cookie_email=nguyenductu@gmail.com'

ck = ck.split(';')
ck = dict([i.strip().split('=') for i in ck])
print (ck)