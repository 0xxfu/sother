interface IERC20 {}

contract BadMappings {
    mapping(address => mapping(address => string)) public badMapping;

    mapping(address => uint256) public badMapping2;

    mapping(address => bytes) internal badMapping3;

    mapping(IERC20 => bytes) internal badMapping4;
    mapping(IERC20 => bytes) internal badMapping5;

    uint256 notBad1;
    string notBad2;
    bytes notBad3;
}

contract NotBadMappings {
    mapping(address => bytes) internal notBadMapping1;

    mapping(IERC20 => bytes) internal notBadMapping2;
    uint256 notBad1;
    string notBad2;
    bytes notBad3;
}
