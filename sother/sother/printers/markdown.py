"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import json
import unittest
from collections import OrderedDict
from typing import Tuple, Type

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
    detector_wiki: DetectorWiki, output_result: OutputResult
) -> Tuple[str, str]:
    """
    @return markdown: markdown string
    @return filename: source filename
    """
    markdown = f"\n## {detector_wiki.wiki_title}\n"
    if detector_wiki.wiki_description or detector_wiki.wiki_exploit_scenario:
        markdown += f"\n### description:\n"
    if detector_wiki.wiki_description:
        markdown += f"{detector_wiki.wiki_description}\n"
    if output_result.markdown:
        markdown += f"{output_result.markdown}\n"
    if detector_wiki.wiki_exploit_scenario:
        markdown += f"{detector_wiki.wiki_exploit_scenario}\n"
    markdown += f"\n### recommendation:\n"
    if detector_wiki.wiki_recommendation:
        markdown += f"{detector_wiki.wiki_recommendation}\n"
    markdown += f"\n### location:\n"
    markdown += f"- {output_result.first_markdown_element}\n"
    markdown += f"\n### severity:\n"
    markdown += f"{output_result.impact}\n"
    markdown += f"\n### category:\n"
    markdown += f"{output_result.check}\n"
    return markdown, output_result.get_first_element_file()


class Markdown(AbstractPrinter):
    ARGUMENT = "markdown"  # run the printer with slither.py --ARGUMENT
    HELP = "Print results to markdown file"  # help information
    WIKI = "https://github.com/crytic/slither"

    def output(self, filename: str) -> output.Output:
        info = ""
        detector_results: list[list[dict]] = self.slither.run_detectors()
        detector_wikis = get_all_detector_wikis()

        markdown_files: dict[str, str] = dict()
        for result in detector_results:
            for detector in result:
                output_result = OutputResult(**detector)
                wiki = (
                    detector_wikis[output_result.check]
                    if output_result.check in detector_wikis
                    else None
                )
                (
                    markdown_str,
                    file_path,
                ) = _to_markdown(wiki, output_result)
                if file_path in markdown_files:
                    markdown_files[file_path] += markdown_str
                else:
                    markdown_files[file_path] = markdown_str

        res = self.generate_output(info)
        for md_file in markdown_files:
            file_path = f"{md_file}.audit.md"
            self.info(f" export markdown file -> {file_path}")
            with open(file_path, "w", encoding="utf8") as f:
                f.write(markdown_files[md_file])
            res.add_file(file_path, markdown_files[md_file])

        return res


if __name__ == "__main__":
    unittest.main()
