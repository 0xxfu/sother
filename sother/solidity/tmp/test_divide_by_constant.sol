// SPDX-License-Identifier: MIT
// pragma solidity 0.8.19; // optimize 200

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
