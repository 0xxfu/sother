contract BytesConstants {
    string public constant bad = "Swivel Finance";
    bytes32 public constant notBad = "Swivel Finance";
}

contract CalculateConstants {
    uint256 constant bad = 1 * 10**18;
    uint256 constant bad2 = 10**18;
    uint256 constant bad3 = 1 + 2;
    uint256 constant bad4 = 2 - 1;
    bytes32 constant badKeccak = keccak256("a");
    bytes constant badEncode = abi.encode("a");
    uint256 constant notBad2 = 1;
}

interface ICheckRole {
    function checkOnlyRole(bytes32 role, address sender)
        external
        view
        returns (bool);
}

contract ContstantInKeccak {
    uint256 x;
    ICheckRole public checkRole;

    function bad() public pure returns (bytes memory) {
        return abi.encode("a");
    }

    function bad2() external {
        require(
            checkRole.checkOnlyRole(keccak256("TIMELOCK"), msg.sender),
            "not authorized"
        );
        x = x + 1;
    }

    function notBad(string memory a) public pure returns (bytes memory) {
        return abi.encode(a);
    }

    function notBad2(bytes memory role) external {
        require(
            checkRole.checkOnlyRole(keccak256(role), msg.sender),
            "not authorized"
        );
        x = x + 1;
    }
}
