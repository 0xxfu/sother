contract UnUsedState {
    address payable destination;

    uint256 public unusedState;
    uint256[50] private __gap;

    function transfer() public payable {
        destination.transfer(msg.value);
    }
}

contract UnusedReturnName {
    function bad0() external pure returns (uint256 a) {
        return 1;
    }

    function bad1() external pure returns (uint256 a, uint256 b) {
        a = 1;
        return (a, 1);
    }

    function bad2() external pure returns (uint256 a, uint256 b) {
        b = 1;
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

contract UnusedParameter {
    function bad0(uint256 a, uint256 b) external pure returns (uint256) {
        return a;
    }

    function bad1(uint256 a, uint256 b) external pure {
        a = a + 1;
    }

    function notBad0(uint256 a) internal pure returns (uint256) {
        return a + 1;
    }

    function notBad1(uint256 a, uint256 b) external pure returns (uint256) {
        return notBad0(a) + b;
    }
}
