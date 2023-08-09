contract MemoryInParameters {
    uint256 state;
    string str;
    bytes byt;
    bytes32 byt32;

    constructor(uint256[] memory a){}

    function bad(
        uint256[] memory a,
        uint256[] memory b,
        uint256[] calldata c
    ) external {
        b[0] = 1;
        state = a[0] + b[0] + c[0];
    }

    function bad2(string memory a) external {
        str = a;
    }

    function bad3(bytes memory a) external {
        byt = a;
    }

    function bad4(uint256[] memory a) public pure returns (uint256[] memory) {
        return a;
    }

    function good(
        uint256[] calldata a,
        uint256[] memory b,
        uint256[] calldata c
    ) external {
        b[0] = 1;
        state = a[0] + b[0] + c[0];
    }

    function notBad(uint256 a) external {
        state = a;
    }

    function notBad2(bytes32 a) external {
        byt32 = a;
    }

    function notBad3(uint256[] memory a)
    internal
    pure
    returns (uint256[] memory)
    {
        return a;
    }
}
