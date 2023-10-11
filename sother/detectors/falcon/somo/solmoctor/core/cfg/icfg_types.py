import typing as T

from slither.core.cfg.node import Node as FalconNode
from slither.slithir.operations import *
from slither.slithir.operations.operation import Operation as FalconIR
from slither.slithir.variables import *
from typing_extensions import TypeAlias

from .defined_node import StateVariableWrapper, EntryPoint, ExitPoint

# All the nodes union in the ICFG
GeneralNode: TypeAlias = T.Union[FalconNode, FalconIR]
ICFGNode: TypeAlias = T.Union[
    FalconNode, FalconIR, StateVariableWrapper, EntryPoint, ExitPoint
]

# All the edges used in the networkx graph
FunctionCallEdge: TypeAlias = T.Tuple[FalconIR, EntryPoint]
CallReturnEdge: TypeAlias = T.Tuple[ExitPoint, FalconIR]
GeneralEdge: TypeAlias = T.Tuple[GeneralNode, GeneralNode]

ICFGEdge: TypeAlias = T.Union[FunctionCallEdge, CallReturnEdge, GeneralEdge]

# Used for the mdg building and contract analysis
ModifierSinkNode: TypeAlias = T.Union[FalconNode, FalconIR]

# The IR operations that could write to the state variables
SlitherLValue: TypeAlias = T.Union[
    StateIRVariable,
    LocalIRVariable,
    TemporaryVariableSSA,
    ReferenceVariableSSA,
    TupleVariableSSA,
]

# The possible operations in the function that can write to the state variables.
FunctionSinkNode: TypeAlias = T.Union[Assignment, Binary, Index]
