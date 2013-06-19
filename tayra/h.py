# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

"""This module is automatically made available inside the template script as
``h``. And the entire namespace is accessible as ``h.<attr>``.

.. code-block:: ttl
    :linenos:

    <head>
    <body>
      ${ h.parsecsv( 'one, two, three' ) }
      ${ h.parsecsvlines( 'one, \\n two, three' ) }

Instead of importing python stdlib modules directly in template scripts it is
better to access them via this module, so that in future when sandboxing
feature is added, your scripts can remain compatible."""

from   pluggdapps.utils.config import *
from   pluggdapps.utils.path import *
from   pluggdapps.utils.asset import *
from   pluggdapps.utils.lib import *
from   pluggdapps.utils.jsonlib import *
from   pluggdapps.utils.parsehttp import *
from   pluggdapps.utils.scaff import *
import os.path as ospath
