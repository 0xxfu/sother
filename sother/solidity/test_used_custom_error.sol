// SPDX-License-Identifier: MIT
pragma solidity 0.8.19;

contract Exception {
    // gas code: 738
    function testRequire(uint256 _i) public pure {
        require(_i > 10, "Input must be greater than 10");
    }

    // gas cost: 694
    function testRevert1(uint256 _i) public pure {
        if (_i <= 10) {
            revert("Input must be greater than 10");
        }
    }

    error TestError();

    // gas code: 462
    function testRevert2(uint256 _i) public pure {
        if (_i <= 10) {
            revert TestError();
        }
    }
}