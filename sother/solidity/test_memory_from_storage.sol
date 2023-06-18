// pragma solidity 0.8.19;

contract StorageMemory {
    struct Foo {
        uint256 x;
    }
    mapping(uint256 => Foo) data;
    uint256 state;
    uint256[] uintArr;

    function bad() external {
        Foo memory f = data[0];
        state = state + 1 + f.x;
    }

    function badArr() external {
        uint256[] memory arr = uintArr;
        arr[0] = 1;
        uintArr = arr;
    }

    function good() external {
        Foo storage f = data[0];
        state = state + 1 + f.x;
    }

    function goodArr() external {
        uint256[] storage arr = uintArr;
        arr[0] = 1;
        uintArr = arr;
    }
}
