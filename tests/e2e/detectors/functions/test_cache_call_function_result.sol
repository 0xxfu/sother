// SPDX-License-Identifier: MIT
contract CallFunctionResult {
    uint256 public state;

    function bad(uint a) external {
        a = a + externalPure();
        a = a + externalPure();
        a = a + publicPure();
        state = a + 1;
    }

    function notBad(uint a) external {
        internalViewPassParam(a);
        internalViewPassParam(a);
        a = a + internalViewPassParam(a);
        a = a + internalViewPassParam(a);
        state = a + 1;
    }

    function good(uint a) external {
        uint256 extPure = externalPure();
        a = a + extPure;
        a = a + extPure;
        state = a + 1;
    }

    function publicPure() public pure returns (uint256) {
        return 10;
    }

    function externalPure() internal pure returns (uint) {
        return 5;
    }

    function internalViewPassParam(uint x) internal pure returns (uint) {
        return x + 1;
    }
}
