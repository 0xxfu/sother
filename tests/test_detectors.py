"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.detectors import get_all_detector_wikis


class DetectorsTestCase(unittest.TestCase):
    def test_detector_wiki(self):
        wikis = get_all_detector_wikis()
        print(wikis)


if __name__ == "__main__":
    unittest.main()
