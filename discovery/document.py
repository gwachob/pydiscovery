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
        self.objects=[]
        self.children=self.rootelem.getchildren()
        for child in self.children:
            if child.tag==XRDNS_S+"Type":
                self.objects.append(Type(child))
            elif child.tag==XRDNS_S+"URI":
                self.objects.append(URI(child))
            elif child.tag==XRDNS_S+"LocalID":
                self.objects.append(LocalID(child))
            else:
                self.objects.append(child)

    def getPriority(self):
        return self.rootelem.get('priority')

    def getContents(self):
        return self.objects

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
        self.objects=[]
        self.children=self.rootelem.getchildren()
        for child in self.children:
            if child.tag==XRDNS_S+"Type":
                self.objects.append(Type(child))
            elif child.tag==XRDNS_S+"Expires":
                self.objects.append(Expires(child))
            elif child.tag==XRDNS_S+"Service":
                self.objects.append(Service(child))
            else:
                self.objects.append(child)

    def getVersion(self):
        return self.rootelem.get("version")

    def getContents(self):
        ''' Returns contents containsing XRD child or extension elements
        '''
        return self.objects

    def getServices(self):
        if self.children is None:
            self.children=self.rootelem.getchildren()
        self.services=[]
        for child in self.children:
            if child.tag==XRDNS_S+"Service":
                self.services.append(Service(child))
        return self.services

class XRDS(DocObject):
    def __init__(self, elem):
        DocObject.__init__(self, elem)
        self.objects=[]
        for child in self.rootelem.getchildren():
            if child.tag==XRDNS_S+"XRD":
                self.objects.append(XRD(child))
            else:
                self.objects.append(child)

    def getContents(self):
        ''' Returns XRD and extension elements
        '''
        return self.objects

