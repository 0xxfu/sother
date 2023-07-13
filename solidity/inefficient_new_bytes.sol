contract InefficientNewBytes {
    bytes byt;

    function bad(bytes memory a) external {
        a = new bytes(0);
        byt = new bytes(0);
    }

    function notBad(bytes memory a) external {
        a = "";
        byt = "";
    }
}
