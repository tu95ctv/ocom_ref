def capf(dh):
    def decor(kkkk):
        def wf(k):
            if dh == "viet hoa":
                k = k.upper()
            elif dh == "viet thuong":
                k = k.lower()
            else:
                k = k.title()
            return kkkk(k)
        return wf
    return inner

@capf("viet hoa")
def stra (input_str):
    return input_str

print (stra("nguyen van nhuan"))

# class textmodify:

#     def __init__(self,thuong_or_hoa):
#         self.thuong_or_hoa = thuong_or_hoa

#     def __call__(self, func):
#         dh = self.thuong_or_hoa
#         def wf(text):
#             k = func(text)
#             if dh == "viet hoa":
#                 k = k.upper()
#             elif dh == "viet thuong":
#                 k = k.lower()
#             else:
#                 k = k.title()
#             return k
#         return wf

# # @textmodify("viet hoa")
# @textmodify("viet thuong")
# def stra(k):
#     return k + ' abc'
# i = stra("Doni Van De Beek")
# print(i)