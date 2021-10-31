# -*- coding: utf-8 -*-
import collections
import threading



__all__ = ['LRU']

class LRU(object):
    """
    Implementation of a length-limited O(1) LRU map.

    Original Copyright 2003 Josiah Carlson, later rebuilt on OrderedDict.
    """
    def __init__(self, count, pairs=()):
        # self._lock = threading.RLock()
        self.count = max(count, 1)
        self.d = collections.OrderedDict()
        for key, value in pairs:
            self[key] = value

    # @synchronized()
    def __contains__(self, obj):
        return obj in self.d

    def get(self, obj, val=None):
        try:
            return self[obj]
        except KeyError:
            return val

    # @synchronized()
    def __getitem__(self, obj):
        a = self.d[obj]
        self.d.move_to_end(obj, last=False)
        return a

    # @synchronized()
    def __setitem__(self, obj, val):
        self.d[obj] = val
        self.d.move_to_end(obj, last=False)
        while len(self.d) > self.count:
            self.d.popitem(last=True)

    # @synchronized()
    def __delitem__(self, obj):
        del self.d[obj]

    # @synchronized()
    def __len__(self):
        return len(self.d)

    # @synchronized()
    def pop(self,key):
        return self.d.pop(key)

    # @synchronized()
    def clear(self):
        self.d.clear()
lru = LRU(1000)

# c = LRU(2)

# c[1] = 1
# c[2] = 1
# c[3] = 1
# print (c.d)
# print (2 in c)
# # print (c[4])
# print (c.d.keys())
# print (c.keys())