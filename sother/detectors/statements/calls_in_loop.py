"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-08
"""
import unittest

from slither.detectors.statements.calls_in_loop import (
    MultipleCallsInLoop as SlitherMultipleCallsInLoop,
)


class MultipleCallsInLoop(SlitherMultipleCallsInLoop):
    WIKI_RECOMMENDATION = "Favor [pull over push](https://ethereum-contract-security-techniques-and-tips.readthedocs.io/en/latest/recommendations/#favor-pull-over-push-for-external-calls) strategy for external calls."


if __name__ == "__main__":
    unittest.main()
