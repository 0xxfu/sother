"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest

from sother.core.models import OutputResult
from sother.detectors.events.missing_sender_in_event import MissingSenderInEvent
from sother.detectors.events.superfluous_fields_event import SuperfluousFieldsEvent
from sother.detectors.operations.use_shifting import DivideByConstant
from sother.detectors.variables.bool_state_variables import BoolStateVariables
from tests.e2e.detectors.detector_testcase import DetectorTestCase


class TestMissingSenderInEvent(DetectorTestCase):
    def test_detect(self):
        results: list[OutputResult] = self.detect(
            f"{self.get_test_solidity_filename(__file__)}.sol",
            MissingSenderInEvent,
        )
        self.check_detect_results(MissingSenderInEvent.WIKI_TITLE, results)


if __name__ == "__main__":
    unittest.main()
