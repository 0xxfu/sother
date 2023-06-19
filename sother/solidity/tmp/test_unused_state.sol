// SPDX-License-Identifier: MIT

contract Uninitialized {
    address payable destination;

    uint256 public unusedState;

    function transfer() public payable {
        destination.transfer(msg.value);
    }
}
