
contract PayableCalls {
    function transfer(address to) external {
        payable(to).transfer(1);
    }

    function send(address to) external {
        payable(to).send(1);

    }
}
