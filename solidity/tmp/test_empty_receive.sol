contract Bad {
    receive() external payable {}
}

contract NotBad {
    address public weth;

    receive() external payable {
        require(msg.sender == address(weth));
    }
}
