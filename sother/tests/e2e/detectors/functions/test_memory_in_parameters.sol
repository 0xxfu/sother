
contract MemoryInParameters {
    uint256 state;

    function bad(
        uint256[] memory a,
        uint256[] memory b,
        uint256[] calldata c
    ) external {
        b[0] = 1;
        state = a[0] + b[0] + c[0];
    }

    function good(
        uint256[] calldata a,
        uint256[] memory b,
        uint256[] calldata c
    ) external {
        b[0] = 1;
        state = a[0] + b[0] + c[0];
    }
}
