"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.events.superfluous_fields_event import SuperfluousFieldsEvent
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestSuperfluousFieldsEvent(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            SuperfluousFieldsEvent,
        )
        self.check_detect_results(SuperfluousFieldsEvent.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
