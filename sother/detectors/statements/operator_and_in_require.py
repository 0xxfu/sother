"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.expressions import BinaryOperation, BinaryOperationType
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings
from sother.utils.gas_utils import GasUtils


class OperatorAndInRequire(AbstractDetector):
    ARGUMENT = "operator-and-in-require"
    HELP = "Splitting `&&` in `require()` statements to saves gas"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Splitting `&&` in `require()` statements to saves gas"
    WIKI_DESCRIPTION = """
Instead of using the `&&` operator in a single require statement to check multiple conditions,using multiple require statements with 1 condition per require statement will save 3 GAS per `&&`

More detail see [this.](https://gist.github.com/0xxfu/478b64036c4cdc45d3d278cd5bd8eb9b)
"""

    WIKI_RECOMMENDATION = """
Splitting `&&` operator in `require()` into multiple `require()` statements.

```
// Before
require(result >= a && result <= b);

// After
require(result >= a);
require(result <= b);
```
"""

    def _detect(self) -> List[Output]:
        results = []
        result_nodes: set[Node] = set()
        for function in GasUtils.get_available_functions(self.compilation_unit):
            if function.name != "requireAnd":
                continue
            for node in function.nodes:
                if not node.contains_require_or_assert():
                    continue

                for ir in node.irs:
                    ir_exp = ir.expression
                    if not isinstance(ir_exp, BinaryOperation):
                        continue
                    if ir_exp.type == BinaryOperationType.ANDAND:
                        result_nodes.add(node)
        for node in result_nodes:
            logger.debug(f"contain `&&` node: {node.expression}")
            res = self.generate_result(
                [
                    node,
                    " contain `&&` operator should be split into multiple `require()` statements.\n",
                ]
            )
            results.append(res)

        return results


if __name__ == "__main__":
    unittest.main()
