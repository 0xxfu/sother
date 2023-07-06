contract Uninitialized{

    function func() external returns(uint){
        uint uint_not_init;
        uint uint_init = 1;
        return uint_not_init + uint_init;
    }    

    function noreportfor() public {
        for(uint i; i < 6; i++) { 
            uint a = i;
        }

        for(uint j = 0; j < 6; j++) { 
            uint b = j;
        }
    }

    function withdraw() payable external {
        address to;
        payable(to).transfer(1);
    }
}

interface IERC20 {
    function transfer(address to, uint256 amount) external returns (bool);

    function transferFrom(
        address from,
        address to,
        uint256 amount
    ) external returns (bool);

    function balanceOf(address account) external view returns (uint256);
}
contract TokenUninitialized {
    IERC20 token;

    function bad0(address to, uint256 amount) external {
        token.transfer(to, amount);
        token.transferFrom(address(this), to, amount);
    }



    function good0(address to, uint256 amount) external {
        uint256 beforeBalance = token.balanceOf(to);
        token.transfer(to, amount);
        token.transferFrom(address(this), to, amount);
        uint256 afterBalance = token.balanceOf(to);
    }

}
