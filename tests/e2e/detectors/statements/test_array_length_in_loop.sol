contract LoopArrayLength {
    uint state;
    uint256[] public stateInts;

    function bad(uint256[] calldata ns) external {
        uint sum = 0;
        for (uint256 i = 0; i < ns.length;) {
            sum += ns[i];
            unchecked {
                i++;
            }
        }
        state = state + ns.length;
    }

    function externalView(uint256[] calldata ns) external returns (uint) {
        uint sum = 0;
        for (uint256 i = 0; i < ns.length;) {
            sum += ns[i];
            stateInts.pop();
            unchecked {
                i++;
            }
        }
        return state;
    }

    function externalPure(uint256[] calldata ns) external pure returns (uint) {
        uint sum = 0;
        for (uint256 i = 0; i < ns.length;) {
            sum += ns[i];
            unchecked {
                i++;
            }
        }
        return sum;
    }

    function internalView(uint256[] calldata ns) internal view returns (uint) {
        uint sum = 0;
        for (uint256 i = 0; i < ns.length;) {
            sum += ns[i];
            unchecked {
                i++;
            }
        }
        return state;
    }

    function good(uint256[] calldata ns) external {
        uint256 length = ns.length;
        uint sum = 0;
        for (uint256 i = 0; i < length;) {
            sum += ns[i];
            unchecked {
                i++;
            }
        }
        state = state + 1;
    }
}
