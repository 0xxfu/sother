import typing as T

import networkx as nx
from slither.core.cfg.node import Node as FalconNode
from slither.core.declarations import Contract, Modifier
from slither.slither import Slither

from sother.detectors.falcon.somo.solmoctor.core.cfg import ICFG_SSA
from sother.detectors.falcon.somo.solmoctor.core.cfg import StateVariableWrapper
from sother.detectors.falcon.somo.solmoctor.core.cfg.icfg_types import ModifierSinkNode


class MDG:
    def __init__(self, contract: Contract, slither_obj: Slither = None) -> None:
        self._contract: Contract = contract
        self._icfg: ICFG_SSA = ICFG_SSA(contract, slither_obj)
        self._mdg_graph: nx.MultiDiGraph = self._icfg.graph
        # Using a dict to record the sink nodes in every modifier.
        self._modifier_analyzing_result: T.Dict[
            Modifier, T.List[ModifierSinkNode]
        ] = dict()

        # filter the function sink nodes in the MDG.
        self._node_filter: T.Callable[
            [FalconNode, nx.MultiDiGraph, str], bool
        ] = lambda node, nx_graph, option_item: nx_graph.nodes[node][option_item]

    @property
    def contract(self) -> Contract:
        return self._contract

    @property
    def name(self) -> str:
        return self.contract.name

    @property
    def icfg(self) -> ICFG_SSA:
        return self._icfg

    @property
    def mdg_graph(self) -> nx.MultiDiGraph:
        return self._mdg_graph

    @property
    def modifier_analyzing_result(self) -> T.Dict[Modifier, T.List[ModifierSinkNode]]:
        return self._modifier_analyzing_result

    @property
    def special_constructor_nodes(self) -> T.List[StateVariableWrapper]:
        return list(
            filter(
                lambda node: isinstance(node, StateVariableWrapper),
                self.mdg_graph.nodes,
            )
        )
