contract IncorrectDeadline {
    function bad0(uint256 deadline) external view {
        if (deadline <= block.timestamp) {
            revert("err");
        }
        if (block.timestamp >= deadline) {
            revert("err");
        }

        uint256 blocktime = block.timestamp;
        if (deadline <= blocktime) {
            revert("err");
        }
    }

    function bad1(uint256 deadline) external view {
        require(deadline > block.timestamp, "err");
        require(block.timestamp < deadline, "err");

        uint256 blocktime = block.timestamp;
        require(deadline > blocktime, "err");
    }

    function notBad(uint256 deadline) external view {
        if (deadline < block.timestamp) {
            revert("err");
        }
        if (block.timestamp > deadline) {
            revert("err");
        }
        if (block.timestamp >= deadline) {
            return;
        }

        uint256 blocktime = block.timestamp;
        if (blocktime > deadline) {
            revert("err");
        }
    }

    function notBad1(uint256 deadline) external view {
        require(deadline >= block.timestamp, "err");
        require(block.timestamp <= deadline, "err");

        uint256 blocktime = block.timestamp;
        require(blocktime <= deadline, "err");
    }
}
