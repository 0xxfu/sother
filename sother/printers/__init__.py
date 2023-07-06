"""
@author: xfu
@email: angerpeanut@gmail.com
@date: 2023-06
"""
import inspect
from typing import Type

from slither.printers import all_printers as slither_all_printers
from slither.printers.abstract_printer import AbstractPrinter

from sother.printers import all_printers


def get_all_printers() -> list[Type[AbstractPrinter]]:
    printers_ = [getattr(all_printers, name) for name in dir(all_printers)]
    printers_ += [
        getattr(slither_all_printers, name)
        for name in dir(slither_all_printers)
    ]
    return [
        p
        for p in printers_
        if inspect.isclass(p) and issubclass(p, AbstractPrinter)
    ]
