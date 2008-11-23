from unittest import TestCase

from discovery.parse import *

class parseXRD(TestCase):
    def __init__(self):
        self.baseXML='''
            <?xml version="1.0" encoding="UTF-8"?>
              <XRDS xmlns="xri://$xrds">
                <XRD xml:id="oauth" xmlns:simple="http://xrds-simple.net/core/1.0" xmlns="xri://$XRD*($v*2.0)" version="2.0">
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
                <XRD xmlns="xri://$XRD*($v*2.0)" version="2.0">
                  <Type>xri://$xrds*simple</Type>
                  <Service priority="10">
                    <Type>http://oauth.net/discovery/1.0</Type>
                    <URI>#oauth</URI>
                  </Service>
                </XRD>
              </XRDS>
                '''
    def test_foo(self):
        assert(1==1)
