
contract UncheckedArrayLength {
    function bad(
        uint256[] calldata arrayA,
        uint256 b,
        uint256[] calldata arrayC
    ) public pure returns (uint256) {
        return 1;
    }

    function notBad(
        uint256[] calldata arrayA,
        uint256 b
    ) public pure returns (uint256) {
        return 1;
    }

    function goodWithRevert(
        uint256[] calldata arrayA,
        uint256 b,
        uint256[] calldata arrayC
    ) public pure returns (uint256) {
        if (arrayA.length != arrayC.length) {
            revert("Length err");
        }
        return 1;
    }

    function goodWithRequire(
        uint256[] calldata arrayA,
        uint256 b,
        uint256[] calldata arrayC
    ) public pure returns (uint256) {
        require(arrayA.length == arrayC.length, "Length err");
        return 1;
    }

    function goodWithAssert(
        uint256[] calldata arrayA,
        uint256 b,
        uint256[] calldata arrayC
    ) public pure returns (uint256) {
        assert(arrayA.length == arrayC.length);
        return 1;
    }
}
