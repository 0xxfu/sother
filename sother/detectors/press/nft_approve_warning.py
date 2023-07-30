"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from slither.analyses.data_dependency.data_dependency import is_dependent
from slither.core.cfg.node import Node
from slither.core.declarations import SolidityVariableComposed
from slither_pess import NftApproveWarning as PressNftApproveWarning


class NftApproveWarning(PressNftApproveWarning):
    def _arbitrary_from(self, nodes: list[Node]):
        """Finds instances of (safe)transferFrom that do not use msg.sender or address(this) as from parameter."""
        irList = []
        for node in nodes:
            for ir in node.irs:
                if hasattr(ir, "function") and hasattr(
                    ir.function, "solidity_signature"
                ):
                    if ir.function.solidity_signature in self._signatures:
                        is_from_sender = is_dependent(
                            ir.arguments[0],
                            SolidityVariableComposed("msg.sender"),
                            node.function.contract,
                        )
                        # is_from_self = is_dependent(ir.arguments[0], SolidityVariable("this"), node.function.contract)
                        if not is_from_sender:  # and not is_from_self
                            irList.append(ir.node)
        return irList


if __name__ == "__main__":
    unittest.main()
