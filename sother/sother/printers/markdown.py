"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import json
import unittest
from collections import OrderedDict

from slither.printers.abstract_printer import AbstractPrinter
from slither.utils import output
from slither.utils.output import Output


class Markdown(AbstractPrinter):
    ARGUMENT = "markdown"  # run the printer with slither.py --ARGUMENT
    HELP = "Print results to markdown file"  # help information
    WIKI = "https://github.com/crytic/slither"

    def output(self, filename: str) -> output.Output:
        info = ""
        all_files = []
        detector_results: list[list[OrderedDict]] = self.slither.run_detectors()
        for item in detector_results:
            # print(f"item: {item}")
            for op in item:
                print(f"dict: {json.dumps(op)}")
        for contract in self.contracts:
            if filename:
                new_filename = f"{filename}-{contract.name}-.md"
            else:
                new_filename = f"dominator-{contract.name}-.md"
            info += f"Export {new_filename}\n"
            content = ""
            for function in contract.functions + contract.modifiers:
                function_content = function.dominator_tree_to_dot(new_filename)
                if function_content is not None:
                    content += function_content + "\n"
            all_files.append((new_filename, content))

        # self.info(info)

        res = self.generate_output(info)
        for filename_result, content in all_files:
            res.add_file(filename_result, content)
        return res


if __name__ == "__main__":
    unittest.main()
