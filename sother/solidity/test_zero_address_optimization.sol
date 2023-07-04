contract Contract0 {
    function bad(address _addr) public pure {
        require(_addr != address(0), "zero address)");
        assert(_addr != address(0));
        if (_addr == address(0)) {
            revert("zero address");
        }
    }

    function notBad(address _addr) public pure {
        _addr = address(0);
    }

    function good(address _addr) public pure {
        assembly {
            if iszero(_addr) {
                mstore(0x00, "zero address")
                revert(0x00, 0x20)
            }
        }
    }
}
