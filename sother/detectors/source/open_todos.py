"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from loguru import logger
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


# todo get `todo` line
class OpenTodos(AbstractDetector):
    ARGUMENT = "open-todos"
    HELP = "OPEN TODOs"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "OPEN TODOs"

    WIKI_DESCRIPTION = """
Open To-dos can point to architecture or programming issues that still
need to be resolved. Often these kinds of comments indicate areas of
complexity or confusion for developers. This provides value and insight
to an attacker who aims to cause damage to the protocol.
"""

    WIKI_RECOMMENDATION = """
Consider resolving the To-dos before deploying code to a production
context. Use an independent issue tracker or other project management
software to track development tasks.
"""

    def _detect(self) -> list[Output]:
        results = []
        todo = "todo"
        for contract in self.compilation_unit.contracts:
            if contract.comments and todo in contract.comments.lower():
                result = self.generate_result(
                    [
                        f"Todo in ",
                        contract,
                        " comments: \n",
                        f"```\n{contract.comments}\n```",
                    ]
                )
                results.append(result)

            if todo in contract.source_mapping.content.lower():
                result = self.generate_result(
                    [
                        f"Todo in ",
                        contract,
                        " content: \n",
                        f"```\n{contract.source_mapping.content}\n```",
                    ]
                )
                results.append(result)

        return results


if __name__ == "__main__":
    unittest.main()
