contract MissingMsgInRequire {
    error CustomError();

    function bad(uint256 a) external {
        require(a > 100);
        revert();

    }

    function good(uint256 a) external {
        require(a > 1000, "cannot < 100");
        revert CustomError();
        revert("revert msg");
    }
}
