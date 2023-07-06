// SPDX-License-Identifier: MIT

contract SmallerUintInt {
    uint256 stateUint256;
    uint128 stateUint128;
    uint64 stateUint64;
    uint32 stateUint32;
    uint16 stateUint16;
    uint8 stateUint8;

    int256 stateint256;
    int128 stateint128;
    int64 stateint64;
    int32 stateint32;
    int16 stateint16;
    int8 stateint8;

    function bad(uint8 _localUint8) external {
        uint256 localUint256;
        uint128 localUint128;
        uint64 localUint64;
        uint32 localUint32;
        uint16 localUint16;
        uint8 localUint8;

        int256 localint256;
        int128 localint128;
        int64 localint64;
        int32 localint32;
        int16 localint16;
        int8 localint8;
    }
}
