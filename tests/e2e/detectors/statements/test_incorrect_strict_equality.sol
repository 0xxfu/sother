abstract contract ERC20Function {
    function balanceOf(address _owner) external virtual returns (uint);
}

contract ERC20Variable {
    mapping(address => uint) public balanceOf;
}


contract ERC20TestBalance {


    function good0(ERC20Function erc) external {
        require(erc.balanceOf(msg.sender) > 0);
    }

    function good1(ERC20Variable erc) external {
        require(erc.balanceOf(msg.sender) > 0);
    }

    function bad0(ERC20Function erc) external {
        require(erc.balanceOf(address(this)) == 10);
    }

    function bad1(ERC20Variable erc) external {
        require(erc.balanceOf(msg.sender) == 10);
    }
}

contract TestContractBalance {

    function bad0() external {
        require(address(address(this)).balance == 10 ether);
        payable(msg.sender).transfer(0.1 ether);
    }

    function bad1() external {
        require(10 ether == address(address(this)).balance);
        payable(msg.sender).transfer(0.1 ether);
    }

    function bad2() external {
        require(address(this).balance == 10 ether);
        payable(msg.sender).transfer(0.1 ether);
    }

    function bad3() external {
        require(10 ether == address(this).balance);
        payable(msg.sender).transfer(0.1 ether);
    }

    function bad4() external {
        uint256 balance = address(this).balance;
        if (balance == 10 ether) {
            payable(msg.sender).transfer(0.1 ether);
        }
    }

    function bad5() external {
        uint256 balance = address(this).balance;
        if (10 ether == balance) {
            payable(msg.sender).transfer(0.1 ether);
        }
    }

    function bad6() external {
        uint256 balance = address(address(this)).balance;
        if (balance == 10 ether) {
            payable(msg.sender).transfer(0.1 ether);
        }
    }

    function myfunc(uint256 balance) pure internal returns (uint256) {
        return balance - balance;
    }

    function good1() external {
        require(address(address(this)).balance >= 10 ether);
        payable(msg.sender).transfer(0.1 ether);
    }

    function good2() external {
        require(10 <= address(address(this)).balance);
        payable(msg.sender).transfer(0.1 ether);
    }

    function good3() external {
        require(address(this).balance >= 10 ether);
        payable(msg.sender).transfer(0.1 ether);
    }

    function good4() external {
        require(10 <= address(this).balance);
        payable(msg.sender).transfer(0.1 ether);
    }

}

contract TestSolidityKeyword {

    function good0() external {
        require(block.timestamp > 0);
    }

    function good1() external {
        require(block.number > 0);
    }

    function good2() external {
        require(block.timestamp > 0);
    }

    function good3(uint param) public {
        // address(this) simulate a particular corner case
        // where the SSA is better
        // the naive data dependency without SSA
        // will consider param and block.number to have a dep
        if (param == 0) {
            param = block.number;
        }
    }

    function notBad() external {
        require(block.timestamp == 0);
    }

    function notBad1() external {
        require(block.number == 0);
    }

    function notBad2() external {
        require(block.number == 0);
    }

}

interface Receiver {

}

contract A {
    mapping(address => Info) data;

    struct Info {
        uint a;
        address b;
        uint c;
    }

    function good(address b) public payable {
        data[msg.sender] = Info(block.timestamp, b, msg.value);
        if (data[msg.sender].b == address(0)) {
            payable(msg.sender).transfer(data[msg.sender].c);
        }
    }

    function good2(address b) public payable {
        data[msg.sender] = Info(block.timestamp, b, msg.value);
        if (Receiver(data[msg.sender].b) == Receiver(address(0))) {
            payable(msg.sender).transfer(data[msg.sender].c);
        }
    }
}