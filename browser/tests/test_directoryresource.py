##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
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
$Id: test_directoryresource.py,v 1.1 2003/08/11 14:58:13 philikon Exp $
"""

import os
from unittest import TestCase, main, makeSuite

from zope.proxy import isProxy, removeAllProxies
from zope.security.checker import NamesChecker
from zope.exceptions import NotFoundError
from zope.publisher.browser import TestRequest

from zope.app.tests.placelesssetup import PlacelessSetup
from zope.app.publisher.browser.directoryresource import \
     DirectoryResourceFactory
from zope.app.publisher.browser.fileresource import FileResource
from zope.app.publisher.browser.pagetemplateresource import \
     PageTemplateResource
import zope.app.publisher.browser.tests as p

test_directory = os.path.split(p.__file__)[0]

checker = NamesChecker(
    ('get', '__getitem__', 'request', 'publishTraverse')
    )

class Test(PlacelessSetup, TestCase):

    def setUp(self):
        PlacelessSetup.setUp(self)

    def testNotFound(self):
        path = os.path.join(test_directory, 'testfiles')
        request = TestRequest()
        resource = DirectoryResourceFactory(path, checker)(request)
        self.assertRaises(NotFoundError, resource.publishTraverse,
                          resource.request, 'doesnotexist')
        self.assertRaises(NotFoundError, resource.get, 'doesnotexist')

    def testGetitem(self):
        path = os.path.join(test_directory, 'testfiles')
        request = TestRequest()
        resource = DirectoryResourceFactory(path, checker)(request)
        self.assertRaises(KeyError, resource.__getitem__, 'doesnotexist')
        file = resource['test.txt']

    def testProxy(self):
        path = os.path.join(test_directory, 'testfiles')
        request = TestRequest()
        resource = DirectoryResourceFactory(path, checker)(request)
        file = resource['test.txt']
        self.assert_(isProxy(file))

    def testCorrectFactories(self):
        path = os.path.join(test_directory, 'testfiles')
        request = TestRequest()
        resource = DirectoryResourceFactory(path, checker)(request)

        image = resource['test.gif']
        self.assert_(isinstance(removeAllProxies(image), FileResource))
        template = resource['test.pt']
        self.assert_(isinstance(removeAllProxies(template), PageTemplateResource))
        file = resource['test.txt']
        self.assert_(isinstance(removeAllProxies(file), FileResource))

def test_suite():
    return makeSuite(Test)

if __name__ == '__main__':
    main(defaultTest='test_suite')
