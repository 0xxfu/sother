// SPDX-License-Identifier: MIT

contract RereadStateVariables {
    uint256 stateUint256;
    uint256 constant SKEWNESS_MASK =                 0x000000000000000000000000000000000000000000000000FFFFFFFFFFFFFFFF; // prettier-ignore
    uint256 constant IS_LONG_SKEWED_MASK =                0x0000000000000000000000000000000000000000000000010000000000000000; // prettier-ignore
    uint256 constant IS_LONG_SKEWED_START_BIT_POSITION = 64;
    uint256 constant MAX_VALID_SKEWNESS = 18446744073709551615;
    event StateEvent(uint256 state, uint256 a);
    struct MarketConfigMap {
        /**
         * bit 0-63: skewness
         * bit 64: is long skewed; true if long
         * bit 65-96: funding rate update timestamp
         * bit 97-126: depth factor: integer(no fixed point)
         * bit 127-156: skewness hard cap: integer(no fixed point)
         * bit 157-186: skewness soft cap: integer(no fixed point)
         * bit 187-194: oracle id
         * bit 195-208: initial margin fraction, bp unit
         * bit 209: market allowance
         */
        uint256 data;
    }

    function bad(uint256 x) external {
        uint256 a = stateUint256 + 1;
        uint256 b = stateUint256 + x;
        stateUint256 = a + b;
    }

    function bad2(uint256 x) external {
        uint256 a = stateUint256 + x;
        emit StateEvent(stateUint256, a);
    }

    function setSkewness(
        MarketConfigMap memory self,
        int256 skewness
    ) internal pure {
        bool isLongSkewed = skewness >= 0;
        uint256 absSkewness = isLongSkewed
            ? uint256(skewness)
            : uint256(0 - skewness);
        require(absSkewness <= MAX_VALID_SKEWNESS);
        self.data = (self.data & ~SKEWNESS_MASK) | absSkewness;
        self.data =
            (self.data & ~IS_LONG_SKEWED_MASK) |
            (uint256(isLongSkewed ? 1 : 0) <<
                IS_LONG_SKEWED_START_BIT_POSITION);
    }

    function notBad(uint256 x) external {
        uint256 a = stateUint256 + 1;
        stateUint256 = x + 1;
        uint256 b = stateUint256 + x;
        stateUint256 = a + b;
    }

    function good(uint256 x) external {
        uint256 tmpState = stateUint256;
        uint256 a = tmpState + 1;
        uint256 b = tmpState + x;
        stateUint256 = a + b;
    }
}
