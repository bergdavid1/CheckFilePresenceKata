from lxml import etree
from unittest import TestCase, mock

import CheckFilePresence

username = 'apiuser'
password = 'PasswordNotNeeded'


class TestClarity(TestCase):
    def test_create_batch_xml_for_post(self):
        file_luids = {'92-164026', '92-164027', '92-164028'}
        clarity = CheckFilePresence.Clarity('roflms801a.mayo.edu')
        xml = clarity.create_batch_xml_for_post(luids=file_luids, link_type='artifacts')

        self.assertIn('<ri:links xmlns:ri="http://genologics.com/ri">', xml)
        self.assertIn('92-164026', xml)
        self.assertIn('<link uri="https://roflms801a.mayo.edu/api/v2/artifacts/92-164028"', xml)

    def test___init___fqdn(self):
        clarity = CheckFilePresence.Clarity('roflms801a.mayo.edu')

        self.assertEqual(
            clarity.base_uri, 'https://roflms801a.mayo.edu/api/v2/',
            "It should properly generate base URI when a FQDN is passed."
        )

    def test___init___good_uri(self):
        clarity = CheckFilePresence.Clarity(
            'https://roflms801a.mayo.edu/api/v2/step/24-12345/details')

        self.assertEqual(
            clarity.base_uri, 'https://roflms801a.mayo.edu/api/v2/',
            "It should extract the base uri from a full uri."
        )

    def test___init___bad_uri(self):
        with self.assertRaisesRegex(
                ValueError,
                "Invalid format for URI. Should be "
                "'https://roflms801a.mayo.edu/api/v2\[/endpoint\]"
        ):
            CheckFilePresence.Clarity('https://roflms801a.mayo.edu/apiv2')

    def test_post_bad_password(self):
        api = CheckFilePresence.Clarity('roflms801a.mayo.edu')
        api.username = 'apiuser'
        api.password = 'BadPassword',
        response_text = "<HTML Stuff>HTTP Status 401 - Bad credentials<HTML Stuff/>"
        response = mock.Mock()
        response.text = response_text

        original_function = CheckFilePresence.requests.post
        CheckFilePresence.requests.post = mock.Mock(return_value=response)

        with self.assertRaisesRegex(UserWarning, 'Bad Credentials'):
            api.post(
                'https://roflms801a.mayo.edu/api/v2/artifacts/batch/retrieve',
                '<tag/>'
            )
        CheckFilePresence.requests.post = original_function

    def test_post_bad_username(self):
        api = CheckFilePresence.Clarity('roflms801a.mayo.edu')
        api.username = 'BadUser'
        api.password = 'BadPassword',
        response_text = "<HTML Stuff>HTTP Status 401 - Bad credentials<HTML Stuff/>"
        response = mock.Mock()
        response.text = response_text

        original_function = CheckFilePresence.requests.post
        CheckFilePresence.requests.post = mock.Mock(return_value=response)

        with self.assertRaisesRegex(UserWarning, 'Bad Credentials'):
            api.post(
                'https://roflms801a.mayo.edu/api/v2/artifacts/batch/retrieve',
                '<tag/>'
            )
        CheckFilePresence.requests.post = original_function

    def test_post_good_credentials_bad_xml(self):
        api = CheckFilePresence.Clarity('roflms801a.mayo.edu')
        api.username = username
        api.password = password

        send_xml = "<this>Bad XML</that>"
        return_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <exc:exception xmlns:exc="http://genologics.com/ri/exception">
                <message>Description of Error from API</message>
            </exc:exception>
            """
        response = mock.Mock()
        response.text = return_xml

        original_function = CheckFilePresence.requests.post
        CheckFilePresence.requests.post = mock.Mock(return_value=response)

        with self.assertRaisesRegex(UserWarning, 'Received API exception. Message:'):
            api.post(
                'https://roflms801a.mayo.edu/api/v2/artifacts/batch/retrieve',
                send_xml
            )
        CheckFilePresence.requests.post = original_function

    def test_post_good_xml(self):

        xml = """
            <ri:links xmlns:ri="http://genologics.com/ri">
              <link uri="https://roflms801a.mayo.edu/api/v2/artifacts/92-164028" rel="artifacts"/>
              <link uri="https://roflms801a.mayo.edu/api/v2/artifacts/92-164027" rel="artifacts"/>
              <link uri="https://roflms801a.mayo.edu/api/v2/artifacts/92-164026" rel="artifacts"/>
            </ri:links>
        """
        return_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <art:details 
                xmlns:art="http://genologics.com/ri/artifact">
                <art:artifact limsid="92-164026">
                    Clipped Content
                </art:artifact>
                <art:artifact limsid="92-164027">
                    Clipped Content
                </art:artifact>
                <art:artifact limsid="92-164028">
                    Clipped Content
                </art:artifact>
            </art:details>
        """
        response = mock.Mock()
        response.text = return_xml

        original_function = CheckFilePresence.requests.post
        CheckFilePresence.requests.post = mock.Mock(return_value=response)

        api = CheckFilePresence.Clarity('roflms801a.mayo.edu')
        api.username = username
        api.password = password

        response_text = api.post(
                'https://roflms801a.mayo.edu/api/v2/artifacts/batch/retrieve',
                xml
        )
        CheckFilePresence.requests.post = original_function

        dom = etree.fromstring(response_text.encode('utf8'))

        self.assertEqual(len(dom.findall('.//art:artifact', dom.nsmap)), 3)
