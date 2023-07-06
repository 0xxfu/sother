"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List, Optional

from loguru import logger
from slither.core.cfg.node import Node, NodeType
from slither.core.declarations import FunctionContract
from slither.core.expressions import UnaryOperationType, UnaryOperation
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
)
from slither.slithir.operations import InternalCall, Length
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings
from sother.utils.gas_utils import GasUtils


def detect_array_length_loop(functions: list[FunctionContract]) -> list[Node]:
    ret: List[Node] = []
    for func in functions:
        array_length_in_loop(func.entry_point, 0, [], ret)
    return ret


def array_length_in_loop(
    node: Optional[Node],
    in_loop_counter: int,
    visited: List[Node],
    ret: List[Node],
) -> None:
    if node is None:
        return

    if node in visited:
        return
    # shared visited
    visited.append(node)

    # check loop start and end
    if node.type == NodeType.STARTLOOP:
        in_loop_counter += 1
    elif node.type == NodeType.ENDLOOP:
        in_loop_counter -= 1

    if in_loop_counter > 0:
        for ir in node.all_slithir_operations():
            exp = ir.expression
            # has ++i/i++ and has checked, detail:https://github.com/crytic/slither/issues/1187
            if (
                isinstance(exp, UnaryOperation)
                and exp.type
                in [
                    UnaryOperationType.PLUSPLUS_POST,
                    UnaryOperationType.PLUSPLUS_PRE,
                    # remove --i/i--
                    # UnaryOperationType.MINUSMINUS_PRE,
                    # UnaryOperationType.MINUSMINUS_POST,
                ]
                and node.scope.is_checked
            ):
                ret.append(ir.node)
                break
            if isinstance(ir, (InternalCall)) and ir.function:
                array_length_in_loop(
                    ir.function.entry_point, in_loop_counter, visited, ret
                )

    for son in node.sons:
        array_length_in_loop(son, in_loop_counter, visited, ret)


class UncheckedInLoop(AbstractDetector):
    ARGUMENT = "unchecked-in-loop"
    HELP = "The increment `++i/i++` in `for-loop`/`while-loop` post condition can be made `unchecked{++i}/unchecked{i++}`"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "The increment `++i/i++` in `for-loop`/`while-loop` post condition can be made `unchecked{++i}/unchecked{i++}`"
    WIKI_DESCRIPTION = """
The unchecked keyword is new in solidity version 0.8.0, so this only applies to that version or higher, which these instances are. 
Gas savings: roughly speaking this can save 30-40 gas per loop iteration. For lengthy loops, this can be significant!

More detail see [this.](https://gist.github.com/0xxfu/67eb8e3d8fe0b8d35370c1263e606d38)
"""

    WIKI_RECOMMENDATION = """
Using `unchecked{++i}/unchecked{i++}` replace `++i/i++` in loop.
"""

    def _detect(self) -> List[Output]:
        results = []

        result_nodes = detect_array_length_loop(
            GasUtils.get_available_functions(self.compilation_unit)
        )
        for node in result_nodes:
            logger.debug(f"unchecked in loop: {str(node)}")
            res = self.generate_result(
                [
                    node,
                    " should be used `unchecked{++i}/unchecked{i++}`.\n",
                ]
            )
            results.append(res)

        return results


if __name__ == "__main__":
    unittest.main()
