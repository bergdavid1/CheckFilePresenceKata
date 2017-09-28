# import requests
from lxml import etree


class Clarity:
    def __init__(self, host, password=None, username=None):
        self.password = password
        self.username = username
        self.base_uri = 'https://' + host + '/api/v2/'

    def create_batch_xml_for_post(self, luids, link_type):
        """
        Returns XML request for a batch endpoint.  Luids are combined with the 
        base uri to generate link elements.  
        :param luids: iterable object containing luids for the batch request
        :param link_type: type of luids provided
        :return: decoded string output from etree with pretty printing.
        """
        nsmap = {'ri': 'http://genologics.com/ri'}
        dom = etree.Element('{%s}links' % nsmap['ri'], nsmap=nsmap)

        for luid in luids:
            link = etree.Element('link')
            link.attrib['uri'] = self.base_uri + 'artifact/' + luid
            link.attrib['rel'] = link_type
            dom.append(link)

        return etree.tostring(dom, pretty_print=True).decode('utf8')
