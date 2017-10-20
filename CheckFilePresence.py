import requests
from lxml import etree
import logging


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
            link.attrib['uri'] = self.base_uri + 'artifacts/' + luid
            link.attrib['rel'] = link_type
            dom.append(link)

        return etree.tostring(dom, pretty_print=True).decode('utf8')

    def post(self, uri, xml):
        response = requests.post(
            url=uri, data=xml,
            auth=(self.username, self.password),
            headers={'Content-Type': 'application/xml'},
        )

        if 'HTTP Status 401 - Bad credentials' in response.text:
            logging.warning("URI: " + uri)
            logging.warning("Request:\n" + xml)
            logging.warning("Response text:\n" + response.text)
            raise UserWarning('Bad Credentials')

        if 'exc:exception' in response.text:
            dom = etree.fromstring(response.text.encode('utf8'))
            logging.warning("URI: " + uri)
            logging.warning("Request:\n" + xml)
            message = dom.findall('message')[0].text
            logging.warning("Response: " + message)
            logging.warning("Response text:\n" + response.text)
            raise UserWarning('Received API exception. Message: ' + message)

        logging.warning("URI: " + uri)
        logging.info("Request:\n" + xml)
        logging.info("Response text:\n" + response.text)
        return response.text

    def missing_files(self, file_list, artifact_list):
        """
        parse dom to determine which if any are missing.
        look to file:file element, then name element.
        :return: None, or a list of missing filenames.
        """
        pass
