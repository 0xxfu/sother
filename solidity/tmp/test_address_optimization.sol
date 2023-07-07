contract AddressOptimizatioin {
    address addr;

    function bad(address _addr) external {
        if (_addr != address(0)) {
            addr = _addr;
        }
    }

    function bad2() external {
        addr = msg.sender;
    }

    function bad3(uint256 i) external {
        for (uint256 a; a < i; ++a) {
            addr = msg.sender;
        }
    }

    function notBad(address _addr) external {
        assembly {
            sstore(addr.slot, _addr)
        }
    }
}
