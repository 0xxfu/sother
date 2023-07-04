// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19; // optimize 200

/**
 * @title StateVarPlusEqVsEqPlus
 * @author 0xxfu
 */
contract StateVarPlusEqVsEqPlus {
    uint256 varr = 1;
    uint256 varr2 = 2;

    function test() external returns (uint256) {
        uint localUint = 0;
        varr += block.number;
        return varr;
    }

    function test2() external returns (uint256) {
        uint localUint2 = 0;
        varr2 = varr2 + block.number;
        varr -= 0;
        return varr2;
    }
}
