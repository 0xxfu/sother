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
    IERC20[] tokens;


    function bad0(IERC20 _token, address to, uint256 amount) external {
        _token.transfer(to, amount);
        _token.transferFrom(address(this), to, amount);
    }

    function bad1(IERC20 _token, address to, uint256 amount) external {
        _token.safeTransfer(to, amount);
        _token.safeTransferFrom(address(this), to, amount);
    }

    function notBad(address to, uint256 amount) external {
        token.transfer(to, amount);
        token.transferFrom(address(this), to, amount);
        token.safeTransfer(to, amount);
        token.safeTransferFrom(address(this), to, amount);
    }

    function notBad2(address to, uint256 amount) external {
        tokens[0].transfer(to, amount);
        tokens[0].transferFrom(address(this), to, amount);
        tokens[0].safeTransfer(to, amount);
        tokens[0].safeTransferFrom(address(this), to, amount);
    }

    function notBad3(address to, uint256 amount, uint256 tokenId) external {
        IERC20 _token = tokens[tokenId];
        _token.transfer(to, amount);
        _token.transferFrom(address(this), to, amount);
        _token.safeTransfer(to, amount);
        _token.safeTransferFrom(address(this), to, amount);
    }

    function good0(IERC20 _token, address to, uint256 amount) external {
        uint256 beforeBalance = _token.balanceOf(to);
        _token.transfer(to, amount);
        _token.transferFrom(address(this), to, amount);
        uint256 afterBalance = _token.balanceOf(to);
    }

    function good1(IERC20 _token, address to, uint256 amount) external {
        uint256 beforeBalance = _token.balanceOf(to);
        _token.safeTransfer(to, amount);
        _token.safeTransferFrom(address(this), to, amount);
        uint256 afterBalance = _token.balanceOf(to);
    }
}
