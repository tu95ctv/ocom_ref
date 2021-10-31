from functools import lru_cache


class A():
    def f(self):
        print ('a')


class B():
    def f(self):
        print ('b')


class C(B,A):
    pass

c = C()
c.f()