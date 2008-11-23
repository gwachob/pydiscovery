from xml.etree import ElementTree as ET
from xml.etree.ElementTree import XML

XRDSNS="xri://$xrds"
XRDNS="xri://$xrd*($v*2.0)"
XRDSNS_S="{%s}" % XRDSNS
XRDNS_S="{%s}" % XRDNS


def parseXRDSString(xmlstring):
    element=XML(xmlstring)
    return XRDS(element)

def parseXRDString(xmlstring):
    element=XML(xmlstring)
    return XRD(element)

class DocObject(object):
    def __init__(self, elem):
        self.rootelem=elem
        self.tag=elem.tag

    def getExtAttributes(self):
        extattributes={}
        for x in self.rootelem.keys():
            if (x.startswith('{')):
                extattributes[x]=self.rootelem.get(x)
        return extattributes

class SimpleDocObject(DocObject):
    def getContent(self):
        return self.rootelem.text

class Type(SimpleDocObject): 
    pass

class Expires(SimpleDocObject):
    pass

class URI(SimpleDocObject):
    pass

class LocalID(SimpleDocObject):
    pass

class Service(DocObject):
    def getPriority(self):
        return self.rootelem.get('priority')

    def getContentIterator(self):
        for child in self.rootelem.getchildren():
            if child.tag==XRDNS_S+"Type":
                yield Type(child)
            elif child.tag==XRDNS_S+"URI":
                yield URI(child)
            elif child.tag==XRDNS_S+"LocalID":
                yield LocalID(child)
            else:
                yield child

class XRD(DocObject):
    def getVersion(self):
        return self.rootelem.get("version")

    def getContentIterator(self):
        ''' Returns an iterator of XRD child or extension elements
        '''
        for child in self.rootelem.getchildren():
            if child.tag==XRDNS_S+"Type":
                yield Type(child)
            elif child.tag==XRDNS_S+"Expires":
                yield Expires(child)
            elif child.tag==XRDNS_S+"Service":
                yield Service(child)
            else:
                yield child

class XRDS(DocObject):
    def getContentIterator(self):
        ''' Returns an iterator of XRD and extension elements
        '''
        for child in self.rootelem.getchildren():
            if child.tag==XRDNS_S+"XRD":
                yield XRD(child)
            else:
                yield child
    
