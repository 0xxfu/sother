contract UseSelfbalance {
    function bad() public returns (uint256) {
        return address(this).balance;
    }

    function bad2(address addr) public {
        uint256 bal = address(addr).balance;
        bal++;
    }

    function notBad() public returns (uint256) {
        assembly {
            let c := selfbalance()
            mstore(0x00, c)
            return(0x00, 0x20)
        }
    }

    function notBad2(address addr) public {
        uint256 bal;
        assembly {
            bal := balance(addr)
        }
        bal++;
    }
}
