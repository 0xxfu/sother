// SPDX-License-Identifier: MIT

contract UnusedInternalFunction {
    uint state;

    function bad(uint a) internal {
        state = state + 1;
    }

    function good(uint a) external {
        state = state + a;
        state = internalUsed(a) + state;
    }

    function internalUsed(uint a) internal view returns (uint) {
        return state + a;
    }
}
