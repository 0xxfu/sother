contract UnusedReturnName {
    function bad0() external pure returns (uint256 a) {
        return 1;
    }

    function bad1() external pure returns (uint256 a, uint256 b) {
        a = 1;
        return (a, 1);
    }

    function bad2() external pure returns (uint256 a, uint256 b) {
        return (1, 1);
    }

    function good0() external pure returns (uint256 a) {
        a = 1;
    }

    function good1() external pure returns (uint256 a, uint256 b) {
        a = 1;
        b = 1;
    }
}
