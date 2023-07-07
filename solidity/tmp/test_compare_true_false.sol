contract CompareTrue {
    function bad(bool a) public pure {
        if (a == true) {
            revert();
        }
    }

    function bad2(bool a) public pure {
        if (a == false) {
            revert();
        }
    }

    function notBad(bool a) public pure {
        if (a) {
            revert();
        }
    }

    function notBad2(bool a) public pure {
        if (!a) {
            revert();
        }
    }
}
