from lxml import etree
import unittest

import CheckFilePresence


username = 'apiuser'
password = 'PasswordNeeded'


@unittest.skipIf(
    password == 'PasswordNeeded',
    'Password is required for integration test but do not store in git.')
class TestClarity(unittest.TestCase):
    def setUp(self):
        self.api = CheckFilePresence.Clarity('roflms801a.mayo.edu')
        self.api.username = username
        self.api.password = password

    def test_post_bad_password(self):
        api = self.api
        api.username = 'apiuser'
        api.password = 'BadPassword',

        with self.assertRaisesRegex(UserWarning, 'Bad Credentials'):
            api.post(
                'https://roflms801a.mayo.edu/api/v2/artifacts/batch/retrieve',
                '<tag/>'
            )

    def test_post_bad_username(self):
        api = self.api
        api.username = 'BadUser'
        api.password = 'BadPassword',
        with self.assertRaisesRegex(UserWarning, 'Bad Credentials'):
            api.post(
                'https://roflms801a.mayo.edu/api/v2/artifacts/batch/retrieve',
                '<tag/>'
            )

    def test_post_good_credentials_bad_xml(self):
        api = self.api
        with self.assertRaisesRegex(UserWarning, 'Received API exception. Message:'):
            api.post(
                'https://roflms801a.mayo.edu/api/v2/artifacts/batch/retrieve',
                '<this>Bad XML</that>'
            )

        api = CheckFilePresence.Clarity('roflms801a.mayo.edu')
        api.username = username
        api.password = password

        send_xml = "<this>Bad XML</that>"

        with self.assertRaisesRegex(UserWarning, 'Received API exception. Message:'):
            api.post(
                'https://roflms801a.mayo.edu/api/v2/artifacts/batch/retrieve',
                send_xml
            )

    def test_post_good_xml(self):

        xml = """
            <ri:links xmlns:ri="http://genologics.com/ri">
              <link uri="https://roflms801a.mayo.edu/api/v2/artifacts/92-164028" rel="artifacts"/>
              <link uri="https://roflms801a.mayo.edu/api/v2/artifacts/92-164027" rel="artifacts"/>
              <link uri="https://roflms801a.mayo.edu/api/v2/artifacts/92-164026" rel="artifacts"/>
            </ri:links>
        """

        api = self.api

        response_text = api.post(
                'https://roflms801a.mayo.edu/api/v2/artifacts/batch/retrieve',
                xml
        )
        dom = etree.fromstring(response_text.encode('utf8'))

        self.assertEqual(len(dom.findall('.//art:artifact', dom.nsmap)), 3)
