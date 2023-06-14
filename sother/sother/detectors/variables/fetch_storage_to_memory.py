"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import unittest
from typing import List

from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
)
from slither.utils.output import Output

from sother.detectors.detector_settings import DetectorSettings


class FetchStorageToMemory(AbstractDetector):
    ARGUMENT = "fetch-storage-to-memory"
    HELP = "Using `storage` instead of `memory` for structs/arrays saves gas"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = DetectorSettings.default_wiki

    WIKI_TITLE = (
        "Using `storage` instead of `memory` for structs/arrays saves gas"
    )
    WIKI_DESCRIPTION = """
    When fetching data from a storage location, assigning the data to a `memory` variable causes all fields of the struct/array to be read from storage, which incurs a Gcoldsload (**2100 gas**) for *each* field of the struct/array. If the fields are read from the new memory variable, they incur an additional `MLOAD` rather than a cheap stack read. Instead of declearing the variable with the `memory` keyword, declaring the variable with the `storage` keyword and caching any fields that need to be re-read in stack variables, will be much cheaper, only incuring the Gcoldsload for the fields actually read. The only time it makes sense to read the whole struct/array into a `memory` variable, is if the full struct/array is being returned by the function, is being passed to a function that requires `memory`, or if the array/struct is being read from another `memory` array/struct
    """

    WIKI_RECOMMENDATION = "Fetching data from `storage` directly, don't convert `storage` it to `memory`"

    def _detect(self) -> List[Output]:
        # todo impl storage detect
        return [self.generate_result(self.WIKI_TITLE)]


if __name__ == "__main__":
    unittest.main()
