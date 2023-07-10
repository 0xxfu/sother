pragma solidity 0.8.13;

contract UnsafeAssembly {
    function bad() external pure {
        assembly {
            calldatacopy(0, 0, calldatasize())
        }
    }
}
