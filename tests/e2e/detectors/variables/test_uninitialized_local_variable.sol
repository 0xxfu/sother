contract Uninitialized {

    function func() external returns (uint){
        uint uint_not_init;
        uint uint_init = 1;
        return uint_not_init + uint_init;
    }

    function noreportfor() public {
        for (uint i; i < 6; i++) {
            uint a = i;
        }

        for (uint j = 0; j < 6; j++) {
            uint b = j;
        }
    }

    function withdraw() payable external {
        address to;
        payable(to).transfer(1);
    }

    function notBad(uint256 a) external returns (address){
        address addr;
        if (a == 0) {
            addr = address(0x0);
        } else if (a >= 100) {
            addr = address(0x100);
        }
        return addr;
    }

}
