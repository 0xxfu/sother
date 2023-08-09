contract UseDeleteStatement {
    uint256 ui256;
    int256 i256;
    address addr;
    bool boolean;

    function bad() external {
        ui256 = 0;
        i256 = 0;
        addr = address(0);
        boolean = false;
    }

    function bad2() external {
        uint256 _ui256 = 0;
        int256 _i256 = 0;
        address _addr = address(0);
        bool _boolean = false;
    }

    function notBad() external {
        for (uint i = 0; i < 10;) {
            unchecked{
                ++i;
            }
        }
        delete ui256;
        delete i256;
        delete addr;
        delete boolean;
    }
}
