contract UnsafeDowncast {
    uint256 ui256;
    uint128 ui128;
    uint32 ui32;

    int256 i256;
    int8 i8;

    event Transmitted(uint32 ue);

    error SafeCastOverflowedUintDowncast(uint8 bits, uint256 value);
    error SafeCastOverflowedIntToUint(int256 value);
    error SafeCastOverflowedIntDowncast(uint8 bits, int256 value);
    error SafeCastOverflowedUintToInt(uint256 value);

    function bad(uint256 a) external {
        ui128 = uint128(a);

        ui32 = uint32(block.timestamp);

        emit Transmitted(uint32(uint256(a >> 8)));
    }

    function bad2(uint128 a) public pure returns (uint32) {
        return uint32(a);
    }

    function notBad(uint256 a) external {
        ui128 = toUint128(a);
    }

    function notBad2(uint256 a) external {
        i256 = int256(a);
    }

    function notBad3(uint256 intAddr) external {
        address addr = address(uint160(intAddr));
    }

    function toUint128(uint256 value) internal pure returns (uint128) {
        if (value > type(uint128).max) {
            revert SafeCastOverflowedUintDowncast(128, value);
        }
        return uint128(value);
    }

    function toUint8(uint256 value) internal pure returns (uint8) {
        if (value > type(uint8).max) {
            revert SafeCastOverflowedUintDowncast(8, value);
        }
        return uint8(value);
    }

    function toUint256(int256 value) internal pure returns (uint256) {
        if (value < 0) {
            revert SafeCastOverflowedIntToUint(value);
        }
        return uint256(value);
    }

    function toInt8(int256 value) internal pure returns (int8 downcasted) {
        downcasted = int8(value);
        if (downcasted != value) {
            revert SafeCastOverflowedIntDowncast(8, value);
        }
    }

    function toInt256(uint256 value) internal pure returns (int256) {
        if (value > uint256(type(int256).max)) {
            revert SafeCastOverflowedUintToInt(value);
        }
        return int256(value);
    }
}

contract UnsafeDoubleCast {
    uint256 ui256;
    uint128 ui128;
    uint32 ui32;
    int256 i256;

    function bad00(uint256 a) external {
        ui128 = uint128(uint64(a));

        ui32 = uint32(uint64(block.timestamp));
    }

    function bad2(uint128 a) public pure returns (uint32) {
        return uint32(uint8(a));
    }

    function notBad(uint256 a) external {
        ui128 = toUint128(a);
    }

    function notBad2(uint256 a) external {
        i256 = int256(a);
    }

    function toUint128(uint256 value) internal pure returns (uint128) {
        if (value > type(uint128).max) {
            revert("err");
        }
        return uint128(value);
    }
}
