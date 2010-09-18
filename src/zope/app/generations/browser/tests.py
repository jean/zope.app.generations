##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Generation-browser tests

$Id$
"""
import unittest
import doctest
from zope.app.generations.testing import GenerationsLayer
from zope.app.testing import ztapi, functional
from zope.generations.generations import SchemaManager, generations_key
from zope.generations.interfaces import ISchemaManager

class TestDatabaseSchema(functional.BrowserTestCase):

    def test(self):
        root = self.getRootFolder()._p_jar.root()
        appkey = 'zope.generations.demo'
        root[generations_key][appkey] = 0
        self.commit()
        manager = SchemaManager(0, 3, 'zope.generations.demo')

        ztapi.provideUtility(ISchemaManager, manager, appkey)

        response = self.publish('/++etc++process/@@generations.html',
                                basic='globalmgr:globalmgrpw')
        body = response.getBody()
        body = ' '.join(body.split())
        expect = ('zope.generations.demo</a> </td> '
                  '<td>0</td> <td>3</td> <td>0</td> '
                  '<td> <input type="submit" value=" evolve " '
                  'name="evolve-app-zope.generations.demo"> </td>')
        self.assert_(body.find(expect) > 0)

        response = self.publish('/++etc++process/@@generations.html'
                                '?evolve-app-zope.generations.demo=evolve',
                                basic='globalmgr:globalmgrpw')
        body = response.getBody()
        body = ' '.join(body.split())
        expect = ('zope.generations.demo</a> </td> '
                  '<td>0</td> <td>3</td> <td>1</td> '
                  '<td> <input type="submit" value=" evolve " '
                  'name="evolve-app-zope.generations.demo"> </td>')
        self.assert_(body.find(expect) > 0)

        response = self.publish('/++etc++process/@@generations.html'
                                '?evolve-app-zope.generations.demo=evolve',
                                basic='globalmgr:globalmgrpw')
        body = response.getBody()
        body = ' '.join(body.split())
        expect = ('zope.generations.demo</a> </td> '
                  '<td>0</td> <td>3</td> <td>2</td> '
                  '<td> <input type="submit" value=" evolve " '
                  'name="evolve-app-zope.generations.demo"> </td>')
        self.assert_(body.find(expect) > 0)

        response = self.publish('/++etc++process/@@generations.html'
                                '?evolve-app-zope.generations.demo=evolve',
                                basic='globalmgr:globalmgrpw')
        body = response.getBody()
        body = ' '.join(body.split())
        expect = ('zope.generations.demo</a> </td> '
                  '<td>0</td> <td>3</td> <td>3</td> '
                  '<td> <span>')
        self.assert_(body.find(expect) > 0)

        ztapi.unprovideUtility(ISchemaManager, appkey)



def test_suite():
    TestDatabaseSchema.layer = GenerationsLayer
    return unittest.TestSuite((
        doctest.DocTestSuite('zope.app.generations.browser.managers'),
        doctest.DocTestSuite('zope.app.generations.browser.managerdetails'),
        unittest.makeSuite(TestDatabaseSchema),
        ))
