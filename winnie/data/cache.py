from winnie.debug import printme
from winnie.util import debug, singleton

import memcache

@singleton
class Client(object):
    """
    A class to handle communication, setting, retrieval
    of variables with memcache.

    Usage:

        c = Cache('orcha')
        print c.foo             # None
        c.foo = "lalala"        # Sets 'orcha/foo' to 'lalala' in memcache
        print c.foo             # lalala
    """

    # Separator
    separator = '.'

    def __init__(self, instance_name, connection=('localhost',)):
        
        printme("Setting cache instance name to %s" % instance_name)

        self.__dict__['name'] = instance_name
        self.__dict__['client'] = memcache.Client(connection)
        self.__dict__['index'] = []
        self._update_index()

    def _update_index(self, new=None, delete=False):
        # If delete, remove this key
        if new and delete and new in self.__dict__['index']:
            print "Removing %s from index" % s
            self.__dict__['index'].remove(new)
        # If not delete and unknown key, add to the index
        elif new and not delete and new not in self.__dict__['index']:
            print "Adding %s to index" %  new
            self.__dict__['index'].append(new)
        
        self.__dict__['index'].sort()
        self.__dict__['client'].set(self.form('index'), self.__dict__['index'])
    
    def __getattr__(self, key):
        return self.__dict__['client'].get(self.form(key))

    def __setattr__(self, key, value):
        if len("%s"%value) > 40:
            repr = "%s chars" % len("%s"%value)
        else: repr=value

        print "(Set %s to %s)"%(key,repr)
        self._update_index(new=key,delete=(value==None))
        return self.__dict__['client'].set(self.form(key), value)
    
    def form(self, key):
        str = "%s%s%s" % (self.name, self.separator, key)
        return str
