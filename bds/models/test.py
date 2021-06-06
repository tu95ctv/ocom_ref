# def f(v,kw=1):
#     print (v,kw)

# f(v=3,kw=2)
# from collections import defaultdict
# path = [2,3,4]
# path2 = [2,3,4,5]
# o = defaultdict(int)
# o[1]
# print (o)
# def f(o, key, gb):
#     print (gb)
#     print (key)
#     o.setdefault(key, gb)

# groupby_fields = {
#             f(o, key, gb)
#             for gb in path
#             for key in ('field', 'groupby')
#         }
# print (o)

# import re
# regex_order = re.compile('^(\s*([a-z0-9:_]+|"[a-z0-9:_]+")(\s+(desc|asc))?\s*(,|$))+(?<!,)$', re.I)

# rs = regex_order.search('abc.')
# print (rs.group(0))

# a = {1:2, 3:1, 2:3}
# a = [(1,2), (3,1), (2,3)]
# rs = sorted(a, key=lambda i:i[1])
# print (rs)
# from collections import OrderedDict

# rs = self.env['payroll.wage.history'].read_group([],('department_id','job_id'),('department_id','job_id'), lazy=False)
# dep = self.env['hr.department']
# job = self.env['hr.job']
# rs2 = sorted(rs,key=lambda i: (dep.browse(i['department_id'][0]).name,job.browse(i['job_id'][0]).name))
# g = OrderedDict()
# for i in rs2:
# 	department_id = i['department_id'][0]
# 	g1 = g.setdefault(department_id,[])
# 	g1.append(i)
# g

# class lazy_property(object):
#     """ Decorator for a lazy property of an object, i.e., an object attribute
#         that is determined by the result of a method call evaluated once. To
#         reevaluate the property, simply delete the attribute on the object, and
#         get it again.
#     """
#     def __init__(self, fget):
#         print ('khời tạo lazy')
#         assert not fget.__name__.startswith('__'),\
#             "lazy_property does not support mangled names"
#         self.fget = fget

#     def __get__(self, obj, cls):
#         print ('trong __get__')
#         if obj is None:
#             return self
#         value = self.fget(obj)
#         setattr(obj, self.fget.__name__, value)
#         return value


# class A():

#     @lazy_property
#     def f(self):
#         print ('trong f')
#         return 2
# a = A()
# print (a.f)
# print ('@@222222')
# print (a.f)


# def d(f):
#     print ('da decor')
#     return f


# a=2
# @d
# def f():
#     print ('trong f')

# from operator import attrgetter
# print (attrgetter('__name__'))

# class A():
#     pass
# print (A()._registry)


from collections import defaultdict, OrderedDict


# s = defaultdict(list)
# print (type(s))

# a = {2:1,1:2, 'a':'b'}
# for i in a:
#     print (i)


class MetaModel(type):
    """ The metaclass of all model classes.
        Its main purpose is to register the models per module.
    """

    module_to_models = defaultdict(list)

    def __new__(meta, name, bases, attrs):
        print ('***__new__ ở meta')
        attrs.setdefault('__slots__', ())
        return super().__new__(meta, name, bases, attrs)

    def __init__(self, name, bases, attrs):
        print ('***__init__ ở meta')
        if not self._register:
            self._register = True
            super(MetaModel, self).__init__(name, bases, attrs)
            return

        # if not hasattr(self, '_module'):
        #     assert self.__module__.startswith('odoo.addons.'), \
        #         "Invalid import of %s.%s, it should start with 'odoo.addons'." % (self.__module__, name)
        #     self._module = self.__module__.split('.')[2]

        # Remember which models to instanciate for this module.
        # if self.__module__:
        self.module_to_models[self.__module__].append(self)

        # for key, val in attrs.items():
        #     if isinstance(val, int):
        #         val.args['_module'] = self._module


class B1():
    # f = f()
    pass

class B2():
    # f = f()
    pass


def f():
    print ('trong hàm f')
    return 1
print ('***tạo 1 cái gì đó')
DummyModel = MetaModel('DummyModel', (B1,B2), {'_register': False})
print ('############ đầu tiên là tạo Base Model###################')

class BaseModel(DummyModel):
    b=2

    f = f()
    pass
print ('..........test coi có in trong hàm f không.............. ')
# BaseModel
class BaseModel2(BaseModel):
    a = 1
    pass

class BaseModel3(BaseModel):
    pass

BaseModel3.__bases__ = (BaseModel2,)
print ('a',BaseModel3.a, BaseModel3.b)
# print (MetaModel)

# A = BaseModel()
print ('############B')
print (DummyModel.__base__)
# A = BaseModel()
# print (BaseModel.module_to_models)
