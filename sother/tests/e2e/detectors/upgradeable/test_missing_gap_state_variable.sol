

abstract contract Initializable {

}

contract Buggy is Initializable{

}

contract Proxy {
    uint256[50] private __gap;
}

contract Good is Initializable,Proxy{

}