"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from dataclasses import dataclass, asdict
from typing import Optional, Any

from pydantic import BaseModel, PrivateAttr
from slither.core.source_mapping.source_mapping import Source
from slither.detectors.abstract_detector import DetectorClassification


class OutputSourceMapping(BaseModel):
    start: int
    length: int
    filename_relative: str
    filename_absolute: str
    filename_short: str
    is_dependency: bool
    lines: list[int]
    starting_column: int
    ending_column: int

    def get_location(self):
        lines = f"#L{self.lines[0]}" if len(self.lines) > 0 else ""
        if len(self.lines) > 1:
            lines += f"-L{self.lines[len(self.lines)-1]}"
        return f"{self.filename_relative}{lines}"


class OutputElement(BaseModel):
    type: str
    name: str
    source_mapping: OutputSourceMapping
    type_specific_fields: Optional[dict]
    additional_fields: Optional[dict[str, str]] = (None,)


class OutputResult(BaseModel):
    elements: list[OutputElement]
    description: str
    markdown: str
    first_markdown_element: str
    id: str
    check: str
    impact: str
    confidence: str

    def get_first_element_file(self) -> str:
        if len(self.elements) > 0:
            return self.elements[0].source_mapping.filename_relative
        return "unknow"


class DetectorWiki(BaseModel):
    argument: str
    help: str
    impact: DetectorClassification
    confidence: DetectorClassification

    wiki: str
    wiki_title: str
    wiki_description: str
    wiki_exploit_scenario: str
    wiki_recommendation: str


class SourceMappingTestCase(unittest.TestCase):
    @property
    def source_dict(self):
        return {
            "start": 187,
            "length": 103,
            "filename_relative": "sample.sol",
            "filename_absolute": "/Users/xfu/Documents/Projects/xfu/github/biibiibii/slither/sother/solidity/sample.sol",
            "filename_short": "sample.sol",
            "is_dependency": False,
            "lines": [8, 9, 10],
            "starting_column": 5,
            "ending_column": 6,
        }

    @property
    def element(self):
        return {
            "type": "function",
            "name": "add_v2",
            "source_mapping": self.source_dict,
            "type_specific_fields": {
                "parent": {
                    "type": "contract",
                    "name": "SafeAdd",
                },
                "signature": "add_v2(uint256,uint256)",
            },
            "additional_fields": {
                "target": "function",
                "convention": "mixedCase",
            },
        }

    @property
    def output_result(self):
        return {
            "elements": [self.element],
            "description": "Function SafeAdd.add_v2(uint256,uint256) (sample.sol#8-10) is not in mixedCase\n",
            "markdown": "Function [SafeAdd.add_v2(uint256,uint256)](sample.sol#L8-L10) is not in mixedCase\n",
            "first_markdown_element": "sample.sol#L8-L10",
            "id": "66963efb59490cd9c77c66de2bde0ae488e89a1b1a94cef839de1a0a586e5285",
            "check": "naming-convention",
            "impact": "Informational",
            "confidence": "High",
        }

    def test_source_mapping(self):
        source = OutputSourceMapping(**self.source_dict)
        self.assertEqual(self.source_dict, source.dict())
        self.assertEqual("sample.sol#L8-L10", source.get_location())

    def test_element(self):
        ele = OutputElement(**self.element)
        self.assertEqual(self.element, ele.dict())

    def test_output_result(self):
        result = OutputResult(**self.output_result)
        self.assertEqual(self.output_result, result.dict())


if __name__ == "__main__":
    unittest.main()
