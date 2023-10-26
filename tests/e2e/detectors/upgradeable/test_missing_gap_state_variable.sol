abstract contract Initializable {

}

contract Buggy is Initializable {

}

contract OwnableUpgradeable is Initializable {}

contract Buggy2 is Initializable {
    mapping(address => mapping(uint256 => uint256)) public claimerReward;
    mapping(uint256 => mapping(uint256 => uint256)) public validatorReward;
    mapping(address => mapping(uint256 => uint256)) public lieutenantReward;
    mapping(uint256 => mapping(uint256 => uint256)) public stakerReward;
    mapping(uint256 => uint256) public lastPoolUpdated;
}

contract Buggy3 is OwnableUpgradeable {
    mapping(address => mapping(uint256 => uint256)) public claimerReward;
    mapping(uint256 => mapping(uint256 => uint256)) public validatorReward;
    mapping(address => mapping(uint256 => uint256)) public lieutenantReward;
    mapping(uint256 => mapping(uint256 => uint256)) public stakerReward;
    mapping(uint256 => uint256) public lastPoolUpdated;
}

contract Proxy {
    uint256[50] private __gap;
}

contract Good is Initializable, Proxy {

}