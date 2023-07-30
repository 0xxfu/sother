"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-07
"""
import unittest

from slither_pess import DoubleEntryTokenPossiblity as PressDoubleEntryTokenPossiblity


class DoubleEntryTokenPossiblity(PressDoubleEntryTokenPossiblity):
    def get_tokens_as_params(self, fun):
        res = []  # параметры функции

        for p in fun.parameters:
            if str(p.type) in ["IERC20[]", "address[]"] and p.name is not None:
                res.append(p)

        return res


if __name__ == "__main__":
    unittest.main()
