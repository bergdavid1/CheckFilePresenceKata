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
