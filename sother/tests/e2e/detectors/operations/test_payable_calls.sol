contract PayableCalls {
    function testTransfer(address to) external {
        payable(to).transfer(1);
    }

    function testSend(address to) external {
        payable(to).send(1);
    }
}
