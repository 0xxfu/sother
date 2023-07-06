contract BadConstructor {
    constructor(address _baseImpl) {}
}

contract BadConstructor2 {
    constructor() {}
}

contract NotBadConstructor {
    constructor(address _baseImpl) payable {}
}

contract NotBadConstructor2 {
    constructor() payable {}
}

contract PayableFunctions {
    address public owner;
    modifier onlyOwner() {
        if (owner != msg.sender) {
            revert("not owner");
        }
        _;
    }
    modifier onlyAdmin() {
        if (owner != msg.sender) {
            revert("not admin");
        }
        _;
    }

    function bad() external onlyOwner {}

    function bad2(address _addr) external onlyAdmin {}

    function notBad() external payable onlyOwner {}

    function notBad2(uint256 a) external payable onlyAdmin {}
}
