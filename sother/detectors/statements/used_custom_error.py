"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from loguru import logger
from slither.core.cfg.node import Node
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings
from sother.utils.gas_utils import GasUtils


# invalid
class UsedCustomError(AbstractDetector):
    ARGUMENT = "use-custom-error"
    HELP = "Using custom errors replace `require` or `assert`"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Using custom errors replace `require` or `assert`"
    WIKI_DESCRIPTION = """
Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).
"""

    WIKI_RECOMMENDATION = """
Using custom errors replace `require` or `assert`.
"""

    def _detect(self) -> List[Output]:
        results = []
        result_nodes: list[Node] = []
        for function in GasUtils.get_available_functions(self.compilation_unit):
            for node in function.nodes:
                if node.contains_require_or_assert():
                    result_nodes.append(node)

        for node in result_nodes:
            logger.debug(f"not custom error: {str(node.expression)}")
            res = self.generate_result(
                [
                    node,
                    " should use custom error to save gas.\n",
                ]
            )
            results.append(res)
        return results


if __name__ == "__main__":
    unittest.main()
