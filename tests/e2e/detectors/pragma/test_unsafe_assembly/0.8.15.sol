pragma solidity 0.8.15;

contract NotUnsafeAssembly2 {
    function bad() external pure {
        assembly {
            calldatacopy(0, 0, calldatasize())
        }
    }
}