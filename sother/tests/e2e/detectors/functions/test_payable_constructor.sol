contract Bad {
    constructor(address _baseImpl) {}
}

contract Bad2 {
    constructor() {}
}

contract NotBad {
    constructor(address _baseImpl) payable {}
}

contract NotBad2 {
    constructor() payable {}
}
