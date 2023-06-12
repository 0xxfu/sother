pragma solidity 0.8.18;

library SafeERC20 {
    function safeTransferFrom(IERC20 token, address from, address to, uint256 value) internal {}
}

interface IERC20 {
    function transferFrom(address, address, uint256) external returns(bool);
}

contract ERC20 is IERC20 {
    function transferFrom(address from, address to, uint256 amount) external override returns(bool) {
        return true;
    }
}

contract C {
    using SafeERC20 for IERC20;

    IERC20 immutable erc20;
    address immutable notsend;
    address immutable send;

    constructor() {
        erc20 = new ERC20();
        notsend = address(0x3);
        send = msg.sender;
    }


    function bad3(address from, address to, uint256 amount) external {
        erc20.safeTransferFrom(from, to, amount);
    }

    function bad4(address from, address to, uint256 amount) external {
        SafeERC20.safeTransferFrom(erc20, from, to, amount);
    }

}
