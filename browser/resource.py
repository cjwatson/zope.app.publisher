##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id: resource.py,v 1.6 2003/09/21 17:32:40 jim Exp $
"""
__metaclass__ = type # All classes are new style when run with Python 2.2+

from zope.app import zapi
from zope.app.location import Location
from zope.app.interfaces.services.service import ISite
from zope.app.interfaces.traversing import IContainmentRoot


class Resource(Location):

    def __init__(self, request):
        self.request = request

    def __call__(self):
        name = self.__name__
        if name.startswith('++resource++'):
            name = name[12:]

        site = self.__parent__
        while 1:
            if ISite.isImplementedBy(site):
                break
            if IContainmentRoot.isImplementedBy(site):
                site = None
                break
            site = site.__parent__

        url = str(zapi.getView(site, 'absolute_url', self.request))
        return "%s/@@/%s" % (url, name)
