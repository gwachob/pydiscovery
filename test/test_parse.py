from unittest import TestCase

from discovery.document import *

class parseXRD(TestCase):
    def setUp(self):
        self.baseXML='''<?xml version="1.0" encoding="UTF-8"?>
              <XRDS xmlns="xri://$xrds" xmlns:foo="http://example.com">
                <XRD xml:id="oauth" xmlns:simple="http://xrds-simple.net/core/1.0" xmlns="xri://$xrd*($v*2.0)" version="2.0" foo:attr="blah">
                  <Type>xri://$xrds*simple</Type>
                  <Expires>2008-12-31T23:59:59Z</Expires>
                  <Service priority="10">
                    <Type>http://oauth.net/core/1.0/endpoint/request</Type>
                    <Type>http://oauth.net/core/1.0/parameters/auth-header</Type>
                    <Type>http://oauth.net/core/1.0/parameters/uri-query</Type>
                    <Type>http://oauth.net/core/1.0/signature/PLAINTEXT</Type>
                    <URI>https://api.example.com/session/request</URI>
                  </Service>
                  <Service priority="10">
                    <Type>http://oauth.net/core/1.0/endpoint/authorize</Type>
                    <Type>http://oauth.net/core/1.0/parameters/uri-query</Type>
                    <URI>https://api.example.com/session/login</URI>
                  </Service>
                  <Service priority="10">
                    <Type>http://oauth.net/core/1.0/endpoint/access</Type>
                    <Type>http://oauth.net/core/1.0/parameters/auth-header</Type>
                    <Type>http://oauth.net/core/1.0/parameters/uri-query</Type>
                    <Type>http://oauth.net/core/1.0/signature/PLAINTEXT</Type>
                    <URI>https://api.example.com/session/activate</URI>
                  </Service>
                  <Service priority="10">
                    <Type>http://oauth.net/core/1.0/endpoint/resource</Type>
                    <Type>http://oauth.net/core/1.0/parameters/auth-header</Type>
                    <Type>http://oauth.net/core/1.0/parameters/uri-query</Type>
                    <Type>http://oauth.net/core/1.0/signature/HMAC-SHA1</Type>
                  </Service>
                  <Service priority="10">
                    <Type>http://oauth.net/discovery/1.0/consumer-identity/static</Type>
                    <LocalID>0685bd9184jfhq22</LocalID>
                  </Service>
                </XRD>
                <XRD xmlns="xri://$xrd*($v*2.0)" version="2.0">
                  <Type>xri://$xrds*simple</Type>
                  <Service priority="10">
                    <Type>http://oauth.net/discovery/1.0</Type>
                    <URI>#oauth</URI>
                  </Service>
                </XRD>
              </XRDS>
                '''
    def test_getXRDS(self):
        xrds=parseXRDSString(self.baseXML)
        xrdlist=xrds.getContents()

        # Test xrds.content iterator length
        self.assertEqual(len(xrdlist), 2)
        firstxrd=xrdlist[0]
        secondxrd=xrdlist[1]

        # Test xrd.getExtAttributes
        extattrs=firstxrd.getExtAttributes()
        self.assertEquals(extattrs.get('{http://example.com}attr'), "blah")

        # Test xrds.getXRDByID
        xrd=xrds.getXRDByID("oauth")
        extattrs=xrd.getExtAttributes()
        self.assertEquals(extattrs.get('{http://example.com}attr'), "blah")

        # Test xrd.getversion
        self.assertEqual(firstxrd.getVersion(), "2.0")
        self.assertEqual(secondxrd.getVersion(), "2.0")

        # Test xrd.getContents
        firstlist=firstxrd.getContents()
        self.assertEqual(len(firstlist), 7)

        # Test xrd.getServices
        svclist=firstxrd.getServices()
        self.assertEqual(len(svclist), 5)
        for i in range(len(svclist)):
            svc=svclist[i]
            self.assertEqual(svc.tag, XRDNS_S+"Service")
            self.assertEqual(svc.getTypeList(), firstlist[i+2].getTypeList())

        # Test known element tag parsing
        self.assertEqual(firstlist[0].tag, XRDNS_S+"Type")
        self.assertEqual(firstlist[1].tag, XRDNS_S+"Expires")
        self.assertEqual(firstlist[2].tag, XRDNS_S+"Service")

        # Test service.getTypeList first call
        self.assertEqual(firstlist[2].getTypeList(), [
                    'http://oauth.net/core/1.0/endpoint/request',
                    'http://oauth.net/core/1.0/parameters/auth-header',
                    'http://oauth.net/core/1.0/parameters/uri-query',
                    'http://oauth.net/core/1.0/signature/PLAINTEXT'
                    ])

        # Test service.getTypeList second call
        self.assertEqual(firstlist[2].getTypeList(), [
                    'http://oauth.net/core/1.0/endpoint/request',
                    'http://oauth.net/core/1.0/parameters/auth-header',
                    'http://oauth.net/core/1.0/parameters/uri-query',
                    'http://oauth.net/core/1.0/signature/PLAINTEXT'
                    ])

        # Test service.containsType
        self.assert_(firstlist[2].containsType('http://oauth.net/core/1.0/parameters/uri-query'))

        # Test simple element content parsing
        self.assertEqual(firstlist[0].getContent(), "xri://$xrds*simple")
        self.assertEqual(firstlist[1].getContent(), "2008-12-31T23:59:59Z")

        # Test known attribute attribute parsing
        self.assertEqual(firstlist[2].getPriority(), "10")
        
        # Test parsing a service element
        firstservicelist=firstlist[2].getContents()
        self.assertEqual(len(firstservicelist), 5)
        self.assertEqual(firstservicelist[0].tag, XRDNS_S+"Type")
        self.assertEqual(firstservicelist[4].tag, XRDNS_S+"URI")
        self.assertEqual(firstservicelist[4].getContent(), "https://api.example.com/session/request")
        
        # Test parsing a service element with other child elements
        lastservicelist=firstlist[6].getContents()
        self.assertEqual(lastservicelist[1].tag, XRDNS_S+"LocalID")
        self.assertEqual(lastservicelist[1].getContent(),"0685bd9184jfhq22") 

