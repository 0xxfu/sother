library SafeERC20 {
    function safeApprove(
        IERC20 token,
        address spender,
        uint256 value
    ) internal {}

    function safeIncreaseAllowance(
        IERC20 token,
        address spender,
        uint256 value
    ) internal {}

    function safeDecreaseAllowance(
        IERC20 token,
        address spender,
        uint256 value
    ) internal {}
}

interface IERC20 {
    function allowance(address owner, address spender)
    external
    view
    returns (uint256);

    function approve(address spender, uint256 amount) external returns (bool);
}

contract RevertOnApproveMax {
    using SafeERC20 for IERC20;
    IERC20 sToken;

    function bad(IERC20 token, address spender) external {
        token.approve(spender, type(uint256).max);

        token.safeApprove(spender, type(uint256).max);

        token.safeIncreaseAllowance(spender, type(uint256).max);
    }

    function notBad(IERC20 token, address spender) external {
        token.approve(spender, type(uint96).max);

        token.safeApprove(spender, type(uint96).max);

        token.safeIncreaseAllowance(spender, type(uint96).max);
    }

    function notBad0(address spender) external {
        sToken.approve(spender, type(uint256).max);

        sToken.safeApprove(spender, type(uint256).max);

        sToken.safeIncreaseAllowance(spender, type(uint256).max);
    }
}
