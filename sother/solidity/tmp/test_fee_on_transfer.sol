

library SafeERC20 {
    function safeTransfer(
        IERC20 token,
        address to,
        uint256 value
    ) internal {
        _callOptionalReturn(
            token,
            abi.encodeWithSelector(token.transfer.selector, to, value)
        );
    }

    function safeTransferFrom(
        IERC20 token,
        address from,
        address to,
        uint256 value
    ) internal {
        _callOptionalReturn(
            token,
            abi.encodeWithSelector(token.transferFrom.selector, from, to, value)
        );
    }

    function _callOptionalReturn(IERC20 token, bytes memory data) private {}
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

contract FeeOnTransfer {
    using SafeERC20 for IERC20;
    IERC20 token;

    function bad0(address to, uint256 amount) external {
        token.transfer(to, amount);
        token.transferFrom(address(this), to, amount);
    }

    function bad1(address to, uint256 amount) external {
        token.safeTransfer(to, amount);
        token.safeTransferFrom(address(this), to, amount);
    }

    function good0(address to, uint256 amount) external {
        uint256 beforeBalance = token.balanceOf(to);
        token.transfer(to, amount);
        token.transferFrom(address(this), to, amount);
        uint256 afterBalance = token.balanceOf(to);
    }

    function good1(address to, uint256 amount) external {
        uint256 beforeBalance = token.balanceOf(to);
        token.safeTransfer(to, amount);
        token.safeTransferFrom(address(this), to, amount);
        uint256 afterBalance = token.balanceOf(to);
    }
}
