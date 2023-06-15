// SPDX-License-Identifier: MIT
contract InternalFunctionToInline {
    uint state1;

    function externalFunction(uint abc) external {
        state1 = abc + internalFunction(abc);
        state1 = state1 + internalFunction2(abc);
    }

    function externalFunction2(uint abc) external {
        state1 = abc + internalFunction2(abc);
    }

    function externalFunction3(uint abc) external {
        state1 = state1 + internalFunction2(abc);
        internalFunction3(abc);
    }

    function externalFunction4(uint abc) external {
        state1 += internalFunction4(abc);
    }

    function internalFunction(uint xyz) internal pure returns (uint256) {
        return xyz + 1;
    }

    function internalFunction2(uint xyz) internal pure returns (uint256) {
        return xyz + 1;
    }

    function internalFunction3(uint xyz) internal pure returns (uint256) {
        return xyz + 1;
    }

    function internalFunction4(uint xyz) internal pure returns (uint256) {
        return xyz + 1;
    }
}
