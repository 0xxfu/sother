library Address {
    error AddressInsufficientBalance(address account);

    error FailedInnerCall();

    function sendValue(address payable recipient, uint256 amount) internal {
        if (address(this).balance < amount) {
            revert AddressInsufficientBalance(address(this));
        }

        (bool success, ) = recipient.call{value: amount}("");
        if (!success) {
            revert FailedInnerCall();
        }
    }
}

contract ReentrancySendValue {
    using Address for address payable;

    function bad(address payable recipient, uint256 ethToSend) external {
        recipient.sendValue(ethToSend);
    }
}
