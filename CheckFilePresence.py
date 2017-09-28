# import requests
from lxml import etree


class Clarity:
    def __init__(self, host, username=None, password=None):
        """
        Initializes instance values required for API authentication.
        TODO... Look into use of class attributes.
        :param host: FQDN or full URI of api endpoint. 
        :param username: username of account with API access
        :param password: password for specified API account
        """
        self.password = password
        self.username = username
        parts = host.split('/')
        if len(parts) == 1:
            self.base_uri = 'https://' + host + '/api/v2/'
        elif 1 < len(parts) < 5:
            raise(
                ValueError(
                    "Invalid format for URI. Should be "
                    "'https://roflms801a.mayo.edu/api/v2[/endpoint]"
                )
            )
        else:
            self.base_uri = '/'.join(parts[0:5]) + '/'

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
