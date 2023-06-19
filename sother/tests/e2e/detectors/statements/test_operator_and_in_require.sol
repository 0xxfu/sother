// SPDX-License-Identifier: MIT

contract SplittingRequire {


    function requireSplit(uint256 a) public pure {
        // gas: 384
        require(a >= 100, "err");
        // gas: 697
        require(a <= 1000, "err");
        // gas: 723

        // gas cost: 339=723-384
    }

    function requireAnd(uint256 a) public pure {
        // gas: 428
        require(a >= 100 && a <= 1000, "err");
        // gas: 775

        // gas cost: 347=775-428
    }


}