contract SusceptibleEcrecover {
    function bad(
        bytes32 digest,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) public pure returns (address) {
        return ecrecover(digest, v, r, s);
    }
}
