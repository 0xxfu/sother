"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import re
import unittest
from typing import Optional

from loguru import logger
from packaging import version


class PragmaUtil:
    @classmethod
    def get_version(cls, version_str: str) -> (str, str):
        pattern = r"\d+\.\d+\.\d+"
        matches = re.findall(pattern, version_str)
        if len(matches) >= 2:
            version_1 = matches[0]
            version_2 = matches[1]
            if version.parse(version_1) > version.parse(version_2):
                return version_2, version_1
            return version_1, version_2

        if len(matches) == 1:
            version_1 = matches[0]
            return version_1, None

        return None, None


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
        version7 = ">=0.6.2<0.9.0"
        self.assertEqual(PragmaUtil.get_version(version7), ("0.6.2", "0.9.0"))


if __name__ == "__main__":
    unittest.main()
