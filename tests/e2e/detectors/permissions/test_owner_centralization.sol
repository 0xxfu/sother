contract Centralization {
    address public owner;
    address public test;
    modifier onlyAllowed() {
        require(msg.sender == owner, "permission is denied!");
        _;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "permission is denied!");
        _;
    }

    modifier onlyTest() {
        require(msg.sender == test, "permission is denied!");
        _;
    }

    function bad() external onlyOwner {}

    function bad0() external onlyOwner {}

    function bad2() external onlyAllowed {}

    function notbad() external onlyTest {}
}
