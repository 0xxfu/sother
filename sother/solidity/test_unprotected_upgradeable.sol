contract Initializable {
    uint8 private _initialized;
    bool private _initializing;

    modifier initializer() {
        _;
    }

    function _disableInitializers() internal virtual {
        require(!_initializing, "Initializable: contract is initializing");
        if (_initialized < type(uint8).max) {
            _initialized = type(uint8).max;
        }
    }
}



contract Buggy is Initializable{
    address payable owner;

    function initialize() external initializer{
        require(owner == address(0));
        owner = payable(msg.sender);
    }
    function kill() external{
        require(msg.sender == owner);
        selfdestruct(owner);
    }
}

contract Buggy2 is Initializable{
    address payable owner;
    function initialize() external initializer{
        require(owner == address(0));
        owner = payable(msg.sender);
    }
}




contract Fixed is Initializable{
    address payable owner;
    uint256[50] private __gap;
    constructor() {
        owner = payable(msg.sender);
    }

    function initialize() external initializer{
        require(owner == address(0));
        owner = payable(msg.sender);

    }
    function kill() external{
        require(msg.sender == owner);
        selfdestruct(owner);
    }

    function other_function() external{

    }
}

contract Not_Upgradeable{
}

contract UpgradeableNoDestruct is Initializable{
    address payable owner;

    constructor() {
        owner = payable(msg.sender);
    }

    function initialize() external initializer{
        require(owner == address(0));
        owner = payable(msg.sender);
    }
}

contract Fixed2 is Initializable {
    address payable owner;
    uint256[50] private __gap;
    constructor() initializer {}

    function initialize() external initializer {
        require(owner == address(0));
        owner = payable(msg.sender);
    }

    function kill() external {
        require(msg.sender == owner);
        selfdestruct(owner);
    }
}

contract Fixed3 is Initializable {
    address payable owner;
    uint256[50] private __gap;
    constructor() {
        _disableInitializers();
    }

    function initialize() external initializer {
        require(owner == address(0));
        owner = payable(msg.sender);
    }

    function kill() external {
        require(msg.sender == owner);
        selfdestruct(owner);
    }
}