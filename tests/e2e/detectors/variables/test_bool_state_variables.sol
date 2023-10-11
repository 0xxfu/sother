// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

/**
 * @title BoolStateVars
 * @author 0xxfu
 */

contract MappingBools {
    mapping(uint => bool) data;
    bool data2;

    // optimize 200
    // 43837 gas
    function set_a81(uint idx, bool value) external {
        data[idx] = value;
    }

    // optimize 200
    // 43621 gas
    function set2(bool value) external {
        data2 = value;
    }
}

contract MappingUint8s {
    mapping(uint => uint8) data;
    uint8 data2;

    // optimize 200
    // 43840 gas
    function set_Hl1r(uint idx, uint8 value) external {
        data[idx] = value;
    }

    // optimize 200
    // 43627 gas
    function set2(uint8 value) external {
        data2 = value;
    }
}

contract MappingUint256s {
    mapping(uint => uint) data;
    uint data2;

    // optimize 200
    // *43729 gas*
    function set_2E3(uint idx, uint value) external {
        data[idx] = value;
    }

    // optimize 200
    // *43516* gas
    function set2(uint value) external {
        data2 = value;
    }
}
