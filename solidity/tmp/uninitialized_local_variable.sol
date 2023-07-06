contract Uninitialized {
    function func() external returns (uint256) {
        uint256 uint_not_init;
        uint256 uint_init = 1;
        return uint_not_init + uint_init;
    }

    function noreportfor() public {
        for (uint256 i; i < 6; i++) {
            uint256 a = i;
        }

        for (uint256 j = 0; j < 6; j++) {
            uint256 b = j;
        }
    }

    function withdraw() external payable {
        address to;
        payable(to).transfer(1);
    }
}

contract A {
    address unused;
    address unused2;
    address unused3;
    address unused4;
    address used;
    address readAddress;
    uint256 readInt;
    uint256 usedInt;
}

contract B is A {
    function bad() external view returns (address) {
        return readAddress;
    }

    function good2() external view returns (uint256) {
        return readInt;
    }

    function good() external {
        usedInt = usedInt + 1;
    }

    fallback() external {
        used = address(0);
    }
}
