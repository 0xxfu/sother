interface IERC20Metadata {
    function name() external view returns (string memory);

    function symbol() external view returns (string memory);

    function decimals() external view returns (uint8);
}

contract UnsupportDecimalsToken {
    IERC20Metadata token;

    function bad(IERC20Metadata a) external view returns (uint8) {
        return a.decimals();
    }

    function bad2(IERC20Metadata a) external view returns (string memory) {
        return a.symbol();
    }

    function bad3(IERC20Metadata a) external view returns (string memory) {
        return a.name();
    }

    function notBad() external view returns (uint8) {
        return token.decimals();
    }
}
