from unittest import TestCase

from discovery.document import *

class parseXRD(TestCase):
    def setUp(self):
        self.baseXML='''<?xml version="1.0" encoding="UTF-8"?>
              <XRDS xmlns="xri://$xrds">
                <XRD xml:id="oauth" xmlns:simple="http://xrds-simple.net/core/1.0" xmlns="xri://$xrd*($v*2.0)" version="2.0">
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
        xrdlist=list(xrds.getContentIterator())
        self.assertEqual(len(xrdlist), 2)
        firstxrd=xrdlist[0]
        secondxrd=xrdlist[1]
        self.assertEqual(firstxrd.getVersion(), "2.0")
        self.assertEqual(secondxrd.getVersion(), "2.0")
        firstlist=list(firstxrd.getContentIterator())
        self.assertEqual(len(firstlist), 7)
        self.assertEqual(firstlist[0].tag, XRDNS_S+"Type")
        self.assertEqual(firstlist[1].tag, XRDNS_S+"Expires")
        self.assertEqual(firstlist[2].tag, XRDNS_S+"Service")

        self.assertEqual(firstlist[0].getContent(), "xri://$xrds*simple")
        self.assertEqual(firstlist[1].getContent(), "2008-12-31T23:59:59Z")

        self.assertEqual(firstlist[2].getPriority(), "10")
        firstservicelist=list(firstlist[2].getContentIterator())
        self.assertEqual(len(firstservicelist), 5)
        self.assertEqual(firstservicelist[0].tag, XRDNS_S+"Type")
        self.assertEqual(firstservicelist[4].tag, XRDNS_S+"URI")
        self.assertEqual(firstservicelist[4].getContent(), "https://api.example.com/session/request")

        lastservicelist=list(firstlist[6].getContentIterator())
        self.assertEqual(lastservicelist[1].tag, XRDNS_S+"LocalID")
        self.assertEqual(lastservicelist[1].getContent(),"0685bd9184jfhq22") 
