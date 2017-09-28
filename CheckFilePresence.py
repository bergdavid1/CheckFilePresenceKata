# import requests


class Clarity:
    def __init__(self, host, password=None, username=None):
        self.password = password
        self.username = username
        self.base_uri = 'https://' + host + '/api/v2/'

    def create_batch_xml_for_post(self, luids, link_type):
        xml = '<ri:links xmlns:ri="http://genologics.com/ri">'
        for luid in luids:
            xml += '<link uri="' + self.base_uri + 'artifact/' + luid + '" rel="' + link_type + '"/>'
        xml += '</ri:links>'

        return xml
