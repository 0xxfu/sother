"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List, Tuple

from loguru import logger
from slither.core.cfg.node import Node
from slither.core.declarations import Contract, FunctionContract
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.slithir.operations import TypeConversion, Send, Transfer
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class PayableCalls(AbstractDetector):
    ARGUMENT = "payable-calls"
    HELP = "Don't use `payable.transfer()`/`payable.send()`"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = "Don't use `payable.transfer()`/`payable.send()`"
    WIKI_DESCRIPTION = """
The use of `payable.transfer()` is [heavily frowned upon](https://consensys.net/diligence/blog/2019/09/stop-using-soliditys-transfer-now/) because it can lead to the locking of funds. The `transfer()` call requires that the recipient is either an EOA account, or is a contract that has a `payable` callback. For the contract case, the `transfer()` call only provides 2300 gas for the contract to complete its operations. This means the following cases can cause the transfer to fail:
* The contract does not have a `payable` callback
* The contract's `payable` callback spends more than 2300 gas (which is only enough to emit something)
* The contract is called through a proxy which itself uses up the 2300 gas

Use OpenZeppelin's `Address.sendValue()` instead
"""
    WIKI_EXPLOIT_SCENARIO = """
Any smart contract that uses `transfer()` or `send()` is taking a hard dependency on gas costs by forwarding a fixed amount of gas: `2300`.
```
contract Vulnerable {
    function withdraw(uint256 amount) external {
        // This forwards 2300 gas, which may not be enough if the recipient
        // is a contract and gas costs change.
        msg.sender.transfer(amount);
    }
}
```
"""

    WIKI_RECOMMENDATION = """
Use OpenZeppelin's [Address.sendValue()](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/2271e2c58d007894c5fe23c4f03a95f645ac9175/contracts/utils/Address.sol#L41-L50) instead of `payable.transfer()`/`payable.send()`
"""

    def _detect(self) -> List[Output]:
        results = []
        for c in self.contracts:
            values = self._detect_payable_calls(c)
            for func, nodes in values:
                info: DETECTOR_INFO = ["Payable calls in ", func, ":\n"]

                # sort the nodes to get deterministic results
                nodes.sort(key=lambda x: x.node_id)

                for node in nodes:
                    info += ["\t- ", node, "\n"]

                res = self.generate_result(info)
                results.append(res)

        return results

    @classmethod
    def _detect_payable_calls(
        cls, contract: Contract
    ) -> list[Tuple[FunctionContract, List[Node]]]:
        ret: [Tuple[FunctionContract, list[Node]]] = []
        for f in [f for f in contract.functions if contract == f.contract_declarer]:
            nodes = f.nodes
            payable_nodes = [n for n in nodes if cls._contains_payable_calls(n)]
            if payable_nodes:
                ret.append((f, payable_nodes))
        return ret

    @classmethod
    def _contains_payable_calls(cls, node: Node) -> bool:
        for ir in node.irs:
            if isinstance(ir, (Send, Transfer)):
                if ir.call_value and ir.call_value != 0:
                    logger.debug(f"payable node: {node.expression}")
                    return True
        return False


if __name__ == "__main__":
    unittest.main()
