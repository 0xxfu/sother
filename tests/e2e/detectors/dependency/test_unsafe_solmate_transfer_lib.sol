library SafeTransferLib {
    function safeTransferETH(address to, uint256 amount) internal {
        bool success;

        /// @solidity memory-safe-assembly
        assembly {
            // Transfer the ETH and store if it succeeded or not.
            success := call(gas(), to, amount, 0, 0, 0, 0)
        }

        require(success, "ETH_TRANSFER_FAILED");
    }
}

library SafeTransfer {}

contract Bad {
    using SafeTransferLib for address;
}

contract NotBad {
    using SafeTransfer for address;
}
