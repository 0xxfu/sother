"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import json
import unittest
from collections import OrderedDict
from typing import Tuple, Type

from slither.detectors.abstract_detector import classification_txt
from slither.printers.abstract_printer import AbstractPrinter
from slither.utils import output
from slither.utils.output import Output

from sother.core.models import (
    OutputSourceMapping,
    OutputElement,
    OutputResult,
    DetectorWiki,
)
from sother.detectors import get_all_detector_wikis


def _to_markdown(
    detector_wiki: DetectorWiki, output_results: list[OutputResult]
) -> Tuple[str, str]:
    """
    @return markdown: markdown string
    @return filename: source filename
    """
    if len(output_results) <= 0:
        return "", ""
    markdown = f"\n## {detector_wiki.wiki_title}\n"
    if detector_wiki.wiki_description or detector_wiki.wiki_exploit_scenario:
        markdown += f"\n### description:\n"
    if detector_wiki.wiki_description:
        markdown += f"{detector_wiki.wiki_description}\n\n"

    if len(output_results) <= 1:
        markdown += (
            f"There is `{len(output_results)}` instance of this issue:\n"
        )
    else:
        markdown += (
            f"There are `{len(output_results)}` instances of this issue:\n"
        )
    for result in output_results:
        markdown += f"{result.markdown}\n"

    if detector_wiki.wiki_exploit_scenario:
        markdown += f"#### Exploit scenario\n"
        markdown += f"{detector_wiki.wiki_exploit_scenario}\n"

    markdown += f"\n### recommendation:\n"
    if detector_wiki.wiki_recommendation:
        markdown += f"{detector_wiki.wiki_recommendation}\n"
    markdown += f"\n### location:\n"
    for result in output_results:
        markdown += f"- {result.first_markdown_element}\n"
    markdown += f"\n### severity:\n"
    markdown += f"{classification_txt[detector_wiki.impact]}\n"
    markdown += f"\n### category:\n"
    markdown += f"{detector_wiki.argument}\n"
    return markdown, detector_wiki.argument


class Markdown(AbstractPrinter):
    ARGUMENT = "markdown"  # run the printer with slither.py --ARGUMENT
    HELP = "Print results to markdown file"  # help information
    WIKI = "https://github.com/crytic/slither"

    def output(self, filename: str) -> output.Output:
        info = ""
        detector_results: list[list[dict]] = self.slither.run_detectors()
        detector_wikis = get_all_detector_wikis()

        detector_outputs: dict[str, list[OutputResult]] = dict()
        for result in detector_results:
            for detector in result:
                output_result = OutputResult(**detector)
                if output_result.check in detector_outputs:
                    detector_outputs[output_result.check].append(output_result)
                else:
                    detector_outputs[output_result.check] = [output_result]
        output_markdown = ""
        for detector_check in detector_outputs:
            print(detector_check, len(detector_outputs[detector_check]))
            wiki = (
                detector_wikis[detector_check]
                if detector_check in detector_wikis
                else None
            )
            (
                markdown_str,
                file_path,
            ) = _to_markdown(wiki, detector_outputs[detector_check])
            output_markdown += markdown_str

        res = self.generate_output(info)
        file_path = f"{filename}_audit.md"
        self.info(f" export markdown file -> {file_path}")
        with open(file_path, "w", encoding="utf8") as f:
            f.write(output_markdown)
        res.add_file(file_path, output_markdown)

        return res


if __name__ == "__main__":
    unittest.main()
