// pragma solidity ^0.5.0;

contract UnUsedState {
    address payable destination;

    uint256 public unusedState;

    function transfer() public payable {
        destination.transfer(msg.value);
    }
}
