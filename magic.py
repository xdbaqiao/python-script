#!/usr/bin/env python2
# coding: utf-8

from collections import defaultdict

class my_dict():
    def __init__(self):
        self.d = defaultdict()
 
    def __contains__(self, name):
        return self.d.__contains__(self.get_hash(name))

    def __getitem__(self, name):
        return  self.d.__getitem__(self.get_hash(name))

    def __setitem__(self, name, value):
        return self.d.__setitem__(self.get_hash(name), value)

    def get_hash(self, name):
        return hash(name)
    
    def keys(self):
        print self.d.keys()

class my_bag(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def __getattr__(self, name):
        return self.get(name)

    def __setattr__(self, name, value):
        if name:
            self[name] = value

y = my_dict()
y['test'] = 'Hello world!'
y['test2'] = 'Hello world!'
print y['test']
print 'test' in y 

bag = my_bag()
bag.name = 'hello bag'
print bag.name
print bag.fd
print bag
