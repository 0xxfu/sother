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
from slither.core.variables import StateVariable
from slither.detectors.operations.unused_return_values import (
    UnusedReturnValues as SlitherUnusedReturnValues,
)
from slither.slithir.operations import Unpack
from slither.slithir.variables import TupleVariable


# except ignore returns by statement.
# eg: (a,,c)= functionCalled();
class UnusedReturnValues(SlitherUnusedReturnValues):
    def detect_unused_return_values(
        self, f: FunctionContract
    ) -> List[Node]:  # pylint: disable=no-self-use
        """
            Return the nodes where the return value of a call is unused
        Args:
            f (Function)
        Returns:
            list(Node)
        """

        values_returned = []
        nodes_origin = {}
        # pylint: disable=too-many-nested-blocks
        for n in f.nodes:
            for ir in n.irs:
                if self._is_instance(ir):
                    # if a return value is stored in a state variable, it's ok
                    if ir.lvalue and not isinstance(ir.lvalue, StateVariable):
                        values_returned.append((ir.lvalue, None))
                        nodes_origin[ir.lvalue] = ir
                        # if isinstance(ir.lvalue, TupleVariable):
                        # we iterate the number of elements the tuple has
                        # and add a (variable, index) in values_returned for each of them
                        # for index in range(len(ir.lvalue.type)):
                        #     values_returned.append((ir.lvalue, index))
                # if return TupleVariable and use one of TupleVariable
                # it should remove from anunsed list
                for read in ir.read:
                    remove = (read, None)
                    if remove in values_returned:
                        values_returned.remove(remove)

        return [nodes_origin[value].node for (value, _) in values_returned]


if __name__ == "__main__":
    unittest.main()
