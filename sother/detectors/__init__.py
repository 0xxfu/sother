"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import inspect
import unittest
from typing import Type

from slither.detectors import all_detectors as slither_all_detectors
from slither.detectors.abstract_detector import AbstractDetector

from sother.core.models import DetectorWiki
from sother.detectors import all_detectors


def get_all_detectors() -> list[Type[AbstractDetector]]:
    detectors_ = [getattr(all_detectors, name) for name in dir(all_detectors)]
    detector_names = [name for name in dir(all_detectors)]
    for name in dir(slither_all_detectors):
        # if sother has override slither class, do not append slither class
        if name in detector_names:
            continue
        detectors_.append(getattr(slither_all_detectors, name))
        detector_names.append(name)

    return [
        d
        for d in detectors_
        if inspect.isclass(d) and issubclass(d, AbstractDetector)
    ]


def get_all_detector_wikis() -> dict[str, DetectorWiki]:
    detectors_list = sorted(
        get_all_detectors(),
        key=lambda element: (
            element.IMPACT,
            element.CONFIDENCE,
            element.ARGUMENT,
        ),
    )
    wikis = dict()
    for detector in detectors_list:
        wikis[detector.ARGUMENT] = DetectorWiki(
            argument=detector.ARGUMENT,
            help=detector.HELP,
            impact=detector.IMPACT,
            confidence=detector.CONFIDENCE,
            wiki=detector.WIKI,
            wiki_title=detector.WIKI_TITLE,
            wiki_description=detector.WIKI_DESCRIPTION,
            wiki_exploit_scenario=detector.WIKI_EXPLOIT_SCENARIO,
            wiki_recommendation=detector.WIKI_RECOMMENDATION,
        )
    return wikis


if __name__ == "__main__":
    unittest.main()
