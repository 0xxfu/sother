interface IERC20 {
    function totalSupply() external view returns (uint256);

    function balanceOf(address account) external view returns (uint256);

    function transfer(address to, uint256 amount) external returns (bool);

    function allowance(address owner, address spender)
    external
    view
    returns (uint256);

    function approve(address spender, uint256 amount) external returns (bool);

    function transferFrom(
        address from,
        address to,
        uint256 amount
    ) external returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 value);

    event Approval(
        address indexed owner,
        address indexed spender,
        uint256 value
    );
}


contract DeprecatedSafeApprove {
    IERC20 sERC20;

    function approveERC20(IERC20 erc20, address recipient) external {
        erc20.approve(recipient, 1);
    }

    function notBad(address recipient) external {
        sERC20.approve(recipient, 1);
    }
}
