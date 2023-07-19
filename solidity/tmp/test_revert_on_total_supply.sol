interface IERC20 {
    function totalSupply() external view returns (uint256);
}

contract RevertTotalSupply {
    IERC20 erc20;

    function bad1(IERC20 addr) external view {
        uint256 localUI = 1000;
        localUI / addr.totalSupply();
    }

    function bad2(IERC20 addr) external view {
        uint256 supply = addr.totalSupply();
        uint256 localUI = 1000;
        uint256 abc = localUI / supply;
    }

    function notBad(IERC20 addr) external view {
        if (addr.totalSupply() == 0) {
            revert("supply err");
        }
        uint256 localUI = 1000;
        localUI / addr.totalSupply();
    }

    function notBad2(IERC20 addr) external view {
        uint256 supply = addr.totalSupply();
        if (supply == 0) {
            revert("supply err");
        }
        uint256 localUI = 1000;
        localUI / supply;
    }

    function notBad3(IERC20 addr) external view {
        uint256 supply = addr.totalSupply();
        if (addr.totalSupply() == 0) {
            revert("supply err");
        }
        uint256 localUI = 1000;
        localUI / supply;
    }

    function notBad4(IERC20 addr) external view {
        addr.totalSupply();
    }
}
