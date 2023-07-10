//pragma solidity 0.8.13;
//
//contract UnsafeAssembly {
//    function bad() external pure {
//        assembly {
//            calldatacopy(0, 0, calldatasize())
//        }
//    }
//}
//
//pragma solidity 0.8.10;
//
//contract UnsafeAssembly2 {
//    function bad() external pure {
//        assembly {
//            calldatacopy(0, 0, calldatasize())
//        }
//    }
//}
//
//pragma solidity 0.8.15;
//
//contract NotUnsafeAssembly2 {
//    function bad() external pure {
//        assembly {
//            calldatacopy(0, 0, calldatasize())
//        }
//    }
//}
