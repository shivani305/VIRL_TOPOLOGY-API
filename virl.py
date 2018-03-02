from __future__ import print_function
from flask import Flask
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree
from lxml import etree
import requests
import imp

from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions


app = Flask(__name__)





class Virl_XML_Generation:

    def __init__(self):
        #required lists and values.
        self.x=['management_network', 'AutoNetkit.address_family', 'AutoNetkit.infrastructure_only',
             'AutoNetkit.ipv4_infra_subnet',
             'AutoNetkit.ipv4_infra_prefix', 'AutoNetkit.ipv4_loopback_subnet', 'AutoNetkit.ipv4_loopback_prefix',
             'AutoNetkit.ipv4_vrf_loopback_subnet', 'ipv4_vrf_loopback_prefix', 'AutoNetkit.enable_routing',
             'AutoNetkit.IGP',
             'AutoNetkit.enable_OnePK', 'AutoNetkit.enable_cdp', 'AutoNetkit.enable_mpls_oam']

        self.y = ['String', 'String', 'Boolean', 'String', 'String', 'String', 'String', 'String', 'String', 'Boolean', 'String',
             'Boolean', 'Boolean',
             'Boolean']

        self.b = 100
        self.c = 110
        self.z = ['flat', 'v4', 'false', '10.0.0.0', '8', '192.168.0.0', '22', '172.16.0.0', '24', 'true', 'ospf', 'false',
             'false', 'false']
        self.m=['AutoNetkit.ibgp_role','Autonetkit.IGP','Auto-generate config']
        self.n=['String','String','Boolean']
        self.o = ['peer', 'ospf', 'true']

    def write(self,d,n1, n2):
        return n1, d[n1].index(n2)

    def generator(self,d,a):

        # root element of xml file
        root = Element('topology')
        tree = ElementTree(root)
        root.set('xmlns', 'http://www.cisco.com/VIRL')
        root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        root.set('schemaVersion', '0.95')
        root.set('xsi:schemaLocation', 'http://www.cisco.com/VIRL https://raw.github.com/CiscoVIRL/schema/v0.95/virl.xsd')

        # extensions as child
        extensions = Element('extensions')
        root.append(extensions)

        # subchild of extensions

        for i in range(len(self.x)):
            entry = Element('entry')
            extensions.append(entry)
            entry.set('key', self.x[i])
            entry.set('type', self.y[i])
            entry.text = self.z[i]

        ##nodes and interfaces
        for i in range(1, len(a) + 1):
            # child element of xml file
            node = Element('node')
            root.append(node)
            node.set('name', str('iosv-' + str(i)))
            node.set('type', 'SIMPLE')
            node.set('subtype', 'IOSv')
            node.set('location', str(str(self.b) + ',' + str(self.c)))
            self.b = self.b + 50
            self.c = self.c + 100
            extensions = Element('extensions')
            node.append(extensions)
            for i in range(len(self.m)):
                entry = Element('entry')
                extensions.append(entry)
                entry.set('key', self.m[i])
                entry.set('type', self.n[i])
                entry.text = self.o[i]

            for j in range(1, a[i - 1] + 1):
                interface = Element('interface')
                node.append(interface)
                interface.set('id', str(j - 1))
                interface.set('name', str('GigabitEthernet0/' + str(j)))

        ##annotations
        #annotations = Element('annonations')
        #root.append(annotations)

        for node in d:
            for k in d[node]:
                if int(k) > int(node):
                    q = self.write(d,node,int(k))
                    w = self.write(d,k,int(node))
                    connection = Element('connection')
                    root.append(connection)
                    connection.set('src',
                                   str('/virl:topology/virl:node[' + str(q[0]) + ']/virl:interface[' + str(1 + q[1]) + ']'))
                    connection.set('dst',
                                   str('/virl:topology/virl:node[' + str(w[0]) + ']/virl:interface[' + str(1 + w[1]) + ']'))

        tree.write('hellotest.virl', "UTF-8")

        return self.prettyPrintXml('hellotest.virl')

        # log = open("topology10.virl", "w")
        # print etree.tostring(root)


    def prettyPrintXml(self,xmlFilePathToPrettyPrint):
        assert xmlFilePathToPrettyPrint is not None
        parser = etree.XMLParser(resolve_entities=False, strip_cdata=False)
        document = etree.parse(xmlFilePathToPrettyPrint, parser)
        document.write(xmlFilePathToPrettyPrint, pretty_print=True, encoding='utf-8')
        return api_calls()







#This Topology class which consists of functions for various topologies.
class topology:
    def __init__(self):
        pass

    def linear(self, n):
        n = input("Enter the number of nodes: ")
        interface_list = [2 for i in range(n)]
        interface_list[0] = 1
        interface_list[n - 1] = 1
        # print interface_list
        # print("Node 1 has interface 2")
        connections = {}
        connections[1] = [2]
        for i in range(2, n):
            # if i==n:
            #   connections[i]=1

            # else:
            connections[i] = [i - 1]
            connections[i].append(i + 1)
        i = i + 1
        connections[i] = [i - 1]

        # print ("Node {} has interfaces  {}").format(i,i+1)
        return Virl_XML_Generation().generator(connections,interface_list)
        # print("Node {} has interface {}").format(n,n-1)

    def ring(self, n):
        n = input("Enter the number of nodes: ")
        interface_list = [2 for i in range(n)]
        interface_list[0] = 1
        interface_list[n - 1] = 1
        # print interface_list
        # print("Node 1 has interface 2")
        connections = {}
        for i in range(1, n + 1):
            if i == n:
                connections[i] = [1]

            else:
                connections[i] = [i + 1];

                # print ("Node {} has interfaces  {}").format(i,i+1)
        return Virl_XML_Generation().generator(connections, interface_list)
        # print("Node {} has interface {}").format(n,n-1)

    def custom_1topo(self,n):

        # a=input("Enter number of nodes:")

        set1 = [i for i in range(1, n / 2 + 1)]

        set2 = [i for i in range(n / 2 + 1, n + 1)]

        print("Node List:")
        print(set1 + set2)
        n1 = len(set1)
        n2 = len(set2)
        interface_list1 = [5 for i in range(len(set1))]
        interface_list1[0] = 3
        interface_list1[n1 - 1] = 3

        interface_list2 = [5 for i in range(len(set2))]
        interface_list2[0] = 3
        interface_list2[n2 - 1] = 3

        print
        "List of Number of interfaces at each node in order:"
        interfaces = interface_list1 + interface_list2
        print
        interfaces

        interface_Dict = {}

        interface_Dict[set1[0]] = [set1[1], set2[0], set2[1]]

        for i in range(2, n1):
            interface_Dict[i] = [i - 1, i + 1, set2[i - 2], set2[i - 1], set2[i]]

        interface_Dict[set1[n1 - 1]] = [set1[n1 - 2], set2[n2 - 2], set2[n2 - 1]]

        interface_Dict[set2[0]] = [set1[0], set1[1], set2[1]]

        for i in range(set2[1], n1 + n2):
            interface_Dict[i] = [i - 1, i + 1, set1[i - n1 - 2], set1[i - n1 - 1], set1[i - n1]]

        interface_Dict[set2[n2 - 1]] = [set1[n1 - 2], set1[n1 - 1], set2[n2 - 2]]

        print
        "Interfaces at each node:"
        print
        interface_Dict

        return Virl_XML_Generation().generator(interface_Dict, interfaces)

    def custom_2topo(self,n):
        # a=input("Enter number of nodes:")

        set1 = [i for i in range(1, n / 2 + 1)]

        set2 = [i for i in range(n / 2 + 1, n + 1)]

        print("Node List:")
        print(set1 + set2)
        n1 = len(set1)
        n2 = len(set2)
        interface_list1 = [4 for i in range(len(set1))]
        interface_list1[0] = 2
        interface_list1[n1 - 1] = 3

        interface_list2 = [4 for i in range(len(set2))]
        interface_list2[0] = 3
        interface_list2[n2 - 1] = 2

        print("List of Number of interfaces at each node in order:")
        interfaces = interface_list1 + interface_list2
        print(interfaces)

        interface_Dict = {}

        interface_Dict[set1[0]] = [set1[1], set2[0], set2[1]]

        for i in range(2, n1):
            interface_Dict[i] = [i - 1, i + 1, set2[i - 2], set2[i - 1]]

        interface_Dict[set1[n1 - 1]] = [set1[n1 - 2], set2[n2 - 2], set2[n2 - 1]]

        interface_Dict[set2[0]] = [set1[0], set1[1], set2[1]]

        for i in range(set2[1], n1 + n2):
            interface_Dict[i] = [set1[i - n1 - 1], set1[i - n1], i - 1, i + 1, set1[i - n1 - 1], set1[i - n1]]

        interface_Dict[set2[n2 - 1]] = [set1[n1 - 1], set2[n2 - 2]]

        print("Interfaces at each node:")
        print(interface_Dict)
        return Virl_XML_Generation().generator(interface_Dict, interfaces)






def api_calls():
    base_url = "http://192.168.139.128:19399/ank/rest/process"
    # final_url="/{0}/friendly/{1}/url".format(base_url,any_value_here)

    payload = open('hellotest.virl', 'rb').read()
    response = requests.post(base_url, auth=('uwmadmin', 'password'), data=payload, verify=False)

    return response.content

    #response.raise_for_status()  # ensure we notice bad responses
    #file = open("out.virl", "w")
    #file.write(response.content)
    #file.close()
    #print(response.text)  # TEXT/HTML
    #print(response.status_code, response.reason)  # HTTP


def file_parser():
    data = imp.load_source('name', 'inputfile1')
    if data.Topology=='custom_1':
        #return str(data.number)
        return topology().custom_1topo(data.number)
    if data.Topology=='custom_2':
        return topology().custom_2topo(data.number)
    if data.Topology=='linear':
        return topology().linear(data.number)
    if data.Topology == 'ring':
        return topology().ring(data.number)

    print (data.number)
    print (data.Topology)

def file_create(data):
    file = open("inputfile1", "w")
    file.write(data)
    file.close()
    return file_parser()



@app.route('/xmlvirl',methods=['POST'])
def xml_virl():

    #return ('Hello World!')

    input_file=request.data

    #if request.data:
        #input_file=request.data
    #return str(input_file)
    return file_create(str(input_file))
    #return file_parser(input_file)




if __name__ == '__main__':
    app.run()
