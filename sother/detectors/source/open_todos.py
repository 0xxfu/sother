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
    WIKI_EXPLOIT_SCENARIO = " "

    def _detect(self) -> list[Output]:
        results = []
        todo = "todo"
        for contract in self.compilation_unit.contracts:
            if contract.comments and todo in contract.comments.lower():
                todos_in_comment: list[str] = list()
                for item in contract.comments.split("\n"):
                    if todo in item.lower():
                        todos_in_comment.append(item)
                if len(todos_in_comment) > 0:
                    info = [
                        f"Todo in ",
                        contract,
                        " comments: \n",
                    ]
                    for td in todos_in_comment:
                        info += ["\t- `", td, "`\n"]
                    result = self.generate_result(info)
                    results.append(result)

            if contract.source_mapping.content:
                todos_in_content: list[str] = list()
                for item in contract.source_mapping.content.split("\n"):
                    if any(["*" in item, "//" in item]) and todo in item.lower():
                        todos_in_content.append(item)

                if len(todos_in_content) > 0:
                    info = [
                        f"Todo in ",
                        contract,
                        " content: \n",
                    ]
                    for td in todos_in_content:
                        info += ["\t- `", td, "`\n"]
                    result = self.generate_result(info)
                    results.append(result)

        return results


if __name__ == "__main__":
    unittest.main()
