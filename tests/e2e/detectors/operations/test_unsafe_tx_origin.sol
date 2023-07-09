contract UnsafeTxOrigin {
    function bad() external view returns (address) {
        return tx.origin;
    }

    function notBad() external view returns (address) {
        return msg.sender;
    }
}
