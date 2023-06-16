// SPDX-License-Identifier: MIT

contract UncheckedInLoop {
    uint state;

    function bad(uint256[] calldata ns) external {
        uint sum = 0;
        for (uint256 i = 0; i < ns.length; i++) {
            sum += ns[i];
        }
        for (uint256 i = 0; i < ns.length; ++i) {
            sum += ns[i];
        }

        for (uint256 j = 0; j < ns.length; ) {
            sum += ns[j];
            unchecked {
                j++;
            }
        }
        state = state + ns.length;
    }

    function externalView(uint256[] calldata ns) external view returns (uint) {
        uint sum = 0;
        for (uint256 i = 0; i < ns.length; ) {
            sum += ns[i];
        }
        return state;
    }

    function externalPure(uint256[] calldata ns) external pure returns (uint) {
        uint sum = 0;
        for (uint256 i = 0; i < ns.length; ++i) {
            sum += ns[i];
        }
        return sum;
    }

    function internalView(uint256[] calldata ns) internal view returns (uint) {
        uint sum = 0;
        for (uint256 i = 100; i > 1; i--) {
            sum += ns[i];
        }
        for (uint256 i = 100; i > 1; --i) {
            sum += ns[i];
        }
        return state;
    }

    function good(uint256[] calldata ns) external {
        uint256 length = ns.length;
        uint sum = 0;
        for (uint256 i = 0; i < length; ) {
            sum += ns[i];
            unchecked {
                i++;
            }
        }
        state = state + 1;
    }
}
