// SPDX-License-Identifier: MIT

abstract contract Ownable {

}

abstract contract OwnableUpgradeable {}

contract DeprecatedOwnable is Ownable {}

contract DeprecatedOwnableUpgradeable is OwnableUpgradeable {}

contract DeprecatedTransferOwnerShip {
    address private _owner;
    event OwnershipTransferred(
        address indexed previousOwner,
        address indexed newOwner
    );
    modifier onlyOwner() {
        _checkOwner();
        _;
    }

    function _checkOwner() internal view virtual {
        require(_owner == msg.sender, "Ownable: caller is not the owner");
    }

    function transferOwnership(address newOwner) public virtual onlyOwner {
        require(
            newOwner != address(0),
            "Ownable: new owner is the zero address"
        );
        _transferOwnership(newOwner);
    }

    function _transferOwnership(address newOwner) internal virtual {
        address oldOwner = _owner;
        _owner = newOwner;
        emit OwnershipTransferred(oldOwner, newOwner);
    }
}

contract DeprecatedTransferOwnerShipFixed is DeprecatedTransferOwnerShip {
    address private _pendingOwner;

    function transferOwnership(address newOwner)
        public
        virtual
        override
        onlyOwner
    {
        _pendingOwner = newOwner;
    }

    function _transferOwnership(address newOwner) internal virtual override {
        delete _pendingOwner;
        super._transferOwnership(newOwner);
    }

    function acceptOwnership() external {
        address sender = msg.sender;
        require(
            _pendingOwner == sender,
            "Ownable2Step: caller is not the new owner"
        );
        _transferOwnership(sender);
    }
}
