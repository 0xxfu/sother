abstract contract Initializable {}

contract ImmutableInUpgradeable is Initializable {
    uint256 immutable a;
    address immutable b;

    uint256 c;

    constructor() {
        a = 100;
        b = address(0);
    }
}
