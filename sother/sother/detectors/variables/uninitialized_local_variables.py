"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.declarations import FunctionContract
from slither.core.solidity_types import ElementaryType
from slither.core.variables.local_variable import LocalVariable

from slither.detectors.variables.uninitialized_local_variables import (
    UninitializedLocalVars as SlitherUninitializedLocalVars,
)


class UninitializedLocalVars(SlitherUninitializedLocalVars):
    def _detect_uninitialized(
        self, function: FunctionContract, node: Node, visited: List[Node]
    ) -> None:
        super()._detect_uninitialized(function, node, visited)
        # results => (Function,LocalVariable)
        for result in self.results:
            func, local_var = result
            if not (
                isinstance(local_var, LocalVariable)
                and isinstance(local_var.type, ElementaryType)
                and str(local_var.type) == "address"
            ):
                self.results.remove(result)


if __name__ == "__main__":
    unittest.main()
