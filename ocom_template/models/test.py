# __slots__
class A():
    a = 1
    @classmethod
    def c(cls):
        print('c')

print (A.__dict__)
print (dir(A))
a = A()
a.c()
A.c()

