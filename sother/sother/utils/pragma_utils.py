"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import Optional

from loguru import logger
from packaging import version


class PragmaUtil:
    @classmethod
    def get_version(cls, version_str: str) -> (str, str):
        ops = [">", "=", "^", "<"]

        def _remove_op(p_version) -> Optional[str]:
            if len(p_version) <= 0:
                return
            if p_version[0] in ops:
                p_version = p_version[1:]
                p_version = _remove_op(p_version)
            return p_version

        version_arr: list[str] = []
        for item in version_str.split(" "):
            if len(item) <= 0:
                continue
            version_arr.append(_remove_op(item))
        if len(version_arr) <= 0:
            return None, None

        if len(version_arr) > 1:
            if version.parse(version_arr[0]) > version.parse(version_arr[1]):
                tmp = version_arr[0]
                version_arr[0] = version_arr[1]
                version_arr[1] = tmp

        return (
            version_arr[0],
            version_arr[1] if len(version_arr) > 1 else None,
        )


class TestUpgradeToLatest(unittest.TestCase):
    def test_get_version(self):
        version1 = ">=0.6.2 <0.9.0"
        self.assertEqual(PragmaUtil.get_version(version1), ("0.6.2", "0.9.0"))
        version2 = "<0.9.0 >=0.6.2"
        self.assertEqual(PragmaUtil.get_version(version2), ("0.6.2", "0.9.0"))
        version3 = ">=0.6.2"
        self.assertEqual(PragmaUtil.get_version(version3), ("0.6.2", None))
        version4 = ">0.6.2"
        self.assertEqual(PragmaUtil.get_version(version4), ("0.6.2", None))
        version5 = "<0.6.2"
        self.assertEqual(PragmaUtil.get_version(version5), ("0.6.2", None))
        version6 = " "
        self.assertEqual(PragmaUtil.get_version(version6), (None, None))


if __name__ == "__main__":
    unittest.main()
