from enum import Enum

from slither.core.declarations import SolidityVariableComposed


class UserAccessibleSolidityVariable(Enum):
    msg_value = SolidityVariableComposed("msg.value")
    msg_data = SolidityVariableComposed("msg.data")
