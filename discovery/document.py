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
    def __init__(self, elem):
        DocObject.__init__(self, elem)
        self.types=None
        self.children=None

    def getPriority(self):
        return self.rootelem.get('priority')

    def getContentIterator(self):
        if self.children is None:
            self.children=self.rootelem.getchildren()
        for child in self.children:
            if child.tag==XRDNS_S+"Type":
                yield Type(child)
            elif child.tag==XRDNS_S+"URI":
                yield URI(child)
            elif child.tag==XRDNS_S+"LocalID":
                yield LocalID(child)
            else:
                yield child


    def getTypeList(self):
        ''' Returns a list of strings which are the Type content types 
        '''
        # Not terribly efficient, but whatever
        if not self.types is None:
            return self.types
        types=[]
        for child in self.rootelem.getchildren():
            if child.tag==XRDNS_S+"Type":
                element=Type(child)
                types.append(element.getContent())
        self.types=types
        return types

    def containsType(self, type):
        return type in self.getTypeList()

class XRD(DocObject):
    def __init__(self, elem):
        DocObject.__init__(self, elem)
        self.children=None

    def getVersion(self):
        return self.rootelem.get("version")

    def getContentIterator(self):
        ''' Returns an iterator of XRD child or extension elements
        '''
        if self.children is None:
            self.children=self.rootelem.getchildren()
        for child in self.children:
            if child.tag==XRDNS_S+"Type":
                yield Type(child)
            elif child.tag==XRDNS_S+"Expires":
                yield Expires(child)
            elif child.tag==XRDNS_S+"Service":
                yield Service(child)
            else:
                yield child

    def getServices(self):
        if self.children is None:
            self.children=self.rootelem.getchildren()
        self.services=[]
        for child in self.children:
            if child.tag==XRDNS_S+"Service":
                self.services.append(Service(child))
        return self.services

class XRDS(DocObject):
    def getContentIterator(self):
        ''' Returns an iterator of XRD and extension elements
        '''
        for child in self.rootelem.getchildren():
            if child.tag==XRDNS_S+"XRD":
                yield XRD(child)
            else:
                yield child
    
