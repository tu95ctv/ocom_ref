# print ('{}')

# class A():
#     pass
# print (A._lock)
import collections
# a = {1:2,3:4}
a = collections.OrderedDict()
a[1] = 2
a[3] = 4
a[5] = 4
a.move_to_end(5, last=False)
print (a)
a.popitem(last=True)
print (a)
########