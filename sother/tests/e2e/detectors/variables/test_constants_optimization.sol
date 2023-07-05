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
