// SPDX-License-Identifier: MIT

interface IERC20 {
    function transfer(address to, uint256 amount) external returns (bool);

    function transferFrom(
        address from,
        address to,
        uint256 amount
    ) external returns (bool);
}

interface IERC721 {
    function safeTransferFrom(
        address from,
        address to,
        uint256 tokenId
    ) external;

    function transferFrom(
        address from,
        address to,
        uint256 tokenId
    ) external;
}

contract UnsafeErc721Transfer {
    IERC721 t;

    function bad0(
        address from,
        address to,
        uint256 tokenId
    ) public {
        t.transferFrom(from, to, tokenId);
    }

    function notBad(
        address from,
        uint256 tokenId
    ) public {
        t.transferFrom(from, address(this), tokenId);
    }

    function good0(
        address from,
        address to,
        uint256 tokenId
    ) public {
        t.safeTransferFrom(from, to, tokenId);
    }
}

contract UnsafeErc20Transfer {
    IERC20 t;

    // calling the transfer function
    function bad0() public {
        t.transfer(address(0), 1 ether);
    }

    function good0() public {
        bool a = t.transfer(address(0), 1 ether);
    }

    function good1() public {
        require(t.transfer(address(0), 1 ether), "failed");
    }

    function good2() public {
        assert(t.transfer(address(0), 1 ether));
    }

    function good3() public returns (bool) {
        return t.transfer(address(0), 1 ether);
    }

    function good4() public returns (bool ret) {
        ret = t.transfer(address(0), 1 ether);
    }

    // calling the transferFrom function
    function bad1() public {
        t.transferFrom(address(this), address(0), 1 ether);
    }

    function good5() public {
        bool a = t.transferFrom(address(this), address(0), 1 ether);
    }

    function good6() public {
        require(t.transferFrom(address(this), address(0), 1 ether), "failed");
    }

    function good7() public {
        assert(t.transferFrom(address(this), address(0), 1 ether));
    }

    function good8() public returns (bool) {
        return t.transferFrom(address(this), address(0), 1 ether);
    }

    function good9() public returns (bool ret) {
        ret = t.transferFrom(address(this), address(0), 1 ether);
    }
}
