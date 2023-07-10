pragma solidity 0.8.10;

contract UnsafeAssembly {
    function bad() external pure {
        assembly {
            calldatacopy(0, 0, calldatasize())
        }
    }
}
