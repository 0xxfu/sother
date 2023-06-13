"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from slither import Slither

from sother.core.models import OutputResult
from sother.detectors import get_all_detector_wikis
from sother.detectors.variables.could_be_immutable import CouldBeImmutable


class TestCouldBeImmutable(unittest.TestCase):
    def test_detect(self):
        slither = Slither("test_could_be_immutable.sol")
        slither.register_detector(CouldBeImmutable)
        results = slither.run_detectors()
        detector_wikis = get_all_detector_wikis()
        for detector_result in results:
            for detector in detector_result:
                output_result = OutputResult(**detector)
                print(output_result.description, "\n")
                print(f"wiki title: {detector_wikis[output_result.check].wiki_title}\n")


if __name__ == "__main__":
    unittest.main()
