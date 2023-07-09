contract UncheckedSetters {
    uint256 x;
    uint256 y;
    uint8 z;
    address owner;

    function bad(uint256 a) external {
        x = a;
    }

    function bad2(address newOwner) external {
        owner = newOwner;
    }

    function bad3(uint256 a) external {
        x = a;
        y = a;
    }

    function bad4(uint256 a) external {
        z = uint8(a);
    }

    function notBad(uint256 a) external {
        if (a > 10) {
            revert("err");
        }
        x = a;
    }
}
