contract MissingSenderInEvents {
    event BadEvent(uint256 x);
    event BadEvent(address a, uint256 x);
    event NotBadEvent(address sender, uint256 x);
    modifier onlyOwner() {
        _;
    }

    function _msgSender() internal view virtual returns (address) {
        return msg.sender;
    }

    function bad(uint256 a) external {
        emit BadEvent(a);
    }

    function bad2(uint256 a, address user) external {
        emit BadEvent(user, a);
    }

    function notBad(uint256 a) external {
        emit NotBadEvent(msg.sender, a);
    }

    function notBad2(uint256 a) external {
        emit NotBadEvent(_msgSender(), a);
    }

    function notBad3(uint256 a, address user) external onlyOwner {
        emit BadEvent(user, a);
    }
}
