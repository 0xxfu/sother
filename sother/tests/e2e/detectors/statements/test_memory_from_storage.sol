pragma solidity 0.8.19;

contract StorageMemory {
    struct Foo {
        uint256 x;
    }
    mapping(uint256 => Foo) data;

    // 2564 gas
    function bad_6eP() external view returns (uint256) {
        Foo memory a = data[0];
        return a.x;
    }

    // 2534 gas
    function good_H7A() external view returns (uint256) {
        Foo storage f = data[0];
        return f.x;
    }
}
