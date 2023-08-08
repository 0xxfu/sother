contract DivVsShr {
    uint256 state;

    // x = 999 : 21517 gas
    function good(uint256 x) external {
        require(x != 0);
        uint256 result;
        result = x >> 1;
        state = result;
    }

    // x = 999 : 21537 gas
    function bad(uint256 x) external {
        require(x != 0);
        uint256 result;
        result = x / 2;

        uint256 a = result / 10;
        result = a / result;
        result = result * 2;

        state = result;
    }

    // x = 999 : 21500
    function testDivUnch(uint256 x) external pure returns (uint256) {
        require(x != 0);
        uint256 result;
        unchecked {
            result = x / 2;
        }
        return result;
    }

}


contract MulPower {
    uint256 state;

    function bad(uint256 x) external {
        uint256 a = 2 ** 10;
        uint256 b = x ** 10;
        uint256 c = 2 ** x;
        state = a + b + c;
    }

    function good(uint256 x) external {
        uint256 a = 1 << 10;
        uint256 b = x ** 10;
        uint256 c = 1 << x;
        state = a + b + c;
    }
}
