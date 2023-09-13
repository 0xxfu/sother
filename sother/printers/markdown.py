"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from enum import Enum
from logging import Logger
from typing import Tuple

from slither.detectors.abstract_detector import (
    classification_txt,
    DetectorClassification,
)
from slither.printers.abstract_printer import AbstractPrinter
from slither.utils import output

from sother.core.models import (
    OutputResult,
    DetectorWiki,
)
from sother.detectors import get_all_detector_wikis


class PrintTarget(Enum):
    default = 0
    secure3 = 1
    code4rena = 2


def _to_markdown(
    detector_wiki: DetectorWiki,
    output_results: list[OutputResult],
    target: PrintTarget = PrintTarget.default,
) -> Tuple[str, str]:
    """
    @return markdown: markdown string
    @return filename: source filename
    """
    if len(output_results) <= 0:
        return "", ""
    # sort by first element line
    output_results.sort(key=lambda x: x.first_element_line)

    detector_impact = f"{classification_txt[detector_wiki.impact]}"
    markdown = f"\n## [{detector_impact}] {detector_wiki.wiki_title}\n"
    if detector_wiki.wiki_description or detector_wiki.wiki_exploit_scenario:
        markdown += f"\n### description\n"
    if detector_wiki.wiki_description:
        markdown += f"{detector_wiki.wiki_description}\n\n"

    if len(output_results) <= 1:
        markdown += f"**There is `{len(output_results)}` instance of this issue:**\n\n"
    else:
        markdown += (
            f"**There are `{len(output_results)}` instances of this issue:**\n\n"
        )
    for result in output_results:
        if target == PrintTarget.secure3:
            markdown += f"- {result.markdown_code}\n"
        else:
            markdown += f"- {result.markdown}\n"

    if (
        detector_wiki.wiki_exploit_scenario
        and detector_wiki.wiki_exploit_scenario != " "
    ):
        markdown += f"#### Exploit scenario\n"
        markdown += f"{detector_wiki.wiki_exploit_scenario}\n"

    markdown += f"\n### recommendation\n"
    if detector_wiki.wiki_recommendation:
        markdown += f"{detector_wiki.wiki_recommendation}\n"
    markdown += f"\n### locations\n"
    for result in output_results:
        markdown += f"- {result.first_markdown_element}\n"
    markdown += f"\n### severity\n"
    markdown += f"{detector_impact}\n"
    markdown += f"\n### category\n"
    markdown += f"{detector_wiki.argument}\n"

    markdown += f"\n### confidence\n"
    markdown += f"{classification_txt[detector_wiki.confidence]}\n"

    return markdown, detector_wiki.argument


def _to_summary_markdown(
    detector_wikis: dict[str, DetectorWiki],
    detector_outputs: dict[
        str,
        list[OutputResult],
    ],
) -> str:
    markdown = "## Summary \n\n"

    impact_checks: [str, str] = dict()
    for detector_check in detector_outputs:
        if detector_check not in detector_wikis:
            continue
        wiki = detector_wikis[detector_check]
        if wiki.impact in impact_checks:
            impact_checks[wiki.impact].append(detector_check)
        else:
            impact_checks[wiki.impact] = [detector_check]

    for impact in impact_checks:
        if impact.value <= DetectorClassification.LOW.value:
            markdown += f"### {classification_txt[impact]} Risk Issues\n\n"
            impact_tag = classification_txt[impact][:1]
        elif impact.value == DetectorClassification.OPTIMIZATION.value:
            impact_tag = "G"
            markdown += f"### Gas Optimizations\n\n"
        else:
            impact_tag = "N"
            markdown += f"### Non-critical Issues\n\n"
        markdown += f"|ID|Issues|Instances|\n"
        markdown += f"|---|:---|:---:|\n"
        idx = 0
        for check in impact_checks[impact]:
            wiki = detector_wikis[check]
            markdown += f"| [{impact_tag}-{idx}] | {wiki.wiki_title} | {len(detector_outputs[check])} |\n"
            idx += 1
        markdown += f"\n\n"

    return markdown


class Markdown(AbstractPrinter):
    ARGUMENT = "markdown"  # run the printer with slither.py --ARGUMENT
    HELP = "Print results to markdown file"  # help information
    WIKI = "https://github.com/crytic/slither"

    def __init__(
        self,
        slither: "Slither",
        logger: Logger,
        print_target: PrintTarget = PrintTarget.default,
    ) -> None:
        super().__init__(slither, logger)
        self._print_target = print_target
        logger.info(f"print target => {self._print_target}")

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
        output_markdown += _to_summary_markdown(detector_wikis, detector_outputs)
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
            ) = _to_markdown(wiki, detector_outputs[detector_check], self._print_target)
            output_markdown += markdown_str

        res = self.generate_output(info)
        if filename == ".":
            file_path = f"sother_audit.md"
        else:
            file_path = f"{filename}_audit.md"
        self.info(f" export markdown file -> {file_path}")
        with open(file_path, "w", encoding="utf8") as f:
            f.write(output_markdown)
        res.add_file(file_path, output_markdown)

        return res


class MarkdownSecure3(Markdown):
    ARGUMENT = "secure3"  # run the printer with slither.py --ARGUMENT
    HELP = "Print results to markdown file (Secure3)"  # help information
    WIKI = "https://github.com/crytic/slither"

    def __init__(self, slither: "Slither", logger: Logger) -> None:
        super().__init__(slither, logger, PrintTarget.secure3)


if __name__ == "__main__":
    unittest.main()
