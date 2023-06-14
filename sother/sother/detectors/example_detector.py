import unittest

from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
)


class ExampleDetector(
    AbstractDetector
):  # pylint: disable=too-few-public-methods
    """
    Documentation
    """

    ARGUMENT = "mydetector"  # slither will launch the detector with slither.py --mydetector
    HELP = "Help printed by slither"
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = "https://github.com/crytic/slither/wiki/Detector-Documentation#constant-functions-using-assembly-code"

    WIKI_TITLE = "This is WIKI_TITLE"
    WIKI_DESCRIPTION = "This is WIKI_DESCRIPTION"
    WIKI_EXPLOIT_SCENARIO = "This is WIKI_EXPLOIT_SCENARIO"
    WIKI_RECOMMENDATION = "This is WIKI_RECOMMENDATION"

    def _detect(self):
        info = "This is an example!\n"

        json = self.generate_result(info)

        return [json]


class ExampleTestCase(unittest.TestCase):
    def test_wiki(self):
        str = ""
        if not str:
            print("not str")
        else:
            print("str")


if __name__ == "__main__":
    unittest.main()
