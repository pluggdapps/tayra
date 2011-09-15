# -*- encoding:utf-8 -*-

from   StringIO             import StringIO
from   zope.interface       import implements
from   zope.component       import getGlobalSiteManager
import tayra
from   tayra.ttl.runtime    import StackMachine



def body(  ) :  
  return __m.popbuftext()

__ttlhash = 'da39a3ee5e6b4b0d3255bfef95601890afd80709'
__ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/ttl/test/stdttl/templaterule.ttl'
