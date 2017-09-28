from unittest import TestCase

from CheckFilePresence import Clarity


class TestClarity(TestCase):
    def test_create_batch_xml_for_post(self):
        file_luids = {'92-164026', '92-164027', '92-164028'}
        clarity = Clarity('roflms801a.mayo.edu')
        xml = clarity.create_batch_xml_for_post(luids=file_luids, link_type='artifacts')

        self.assertIn('<ri:links xmlns:ri="http://genologics.com/ri">', xml)
        self.assertIn('92-164026', xml)
        self.assertIn('<link uri="https://roflms801a.mayo.edu/api/v2/artifact/92-164028"', xml)

    def test___init___fqdn(self):
        clarity = Clarity('roflms801a.mayo.edu')

        self.assertEqual(
            clarity.base_uri, 'https://roflms801a.mayo.edu/api/v2/',
            "It should properly generate base URI when a FQDN is passed."
        )

    def test___init___good_uri(self):
        clarity = Clarity('https://roflms801a.mayo.edu/api/v2/step/24-12345/details')

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
            clarity = Clarity('https://roflms801a.mayo.edu/apiv2')
