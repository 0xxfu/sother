interface ISwapRouterBad {
    struct ExactInputSingleParams {
        address tokenIn;
        address tokenOut;
        uint24 fee;
        address recipient;
        // uint256 deadline;
        uint256 amountIn;
        uint256 amountOutMinimum;
        uint160 sqrtPriceLimitX96;
    }

    function exactInputSingle(ExactInputSingleParams calldata params)
    external
    payable
    returns (uint256 amountOut);

    struct ExactInputParams {
        bytes path;
        address recipient;
        // uint256 deadline;
        uint256 amountIn;
        uint256 amountOutMinimum;
    }

    function exactInput(ExactInputParams calldata params)
    external
    payable
    returns (uint256 amountOut);

    struct ExactOutputSingleParams {
        address tokenIn;
        address tokenOut;
        uint24 fee;
        address recipient;
        // uint256 deadline;
        uint256 amountOut;
        uint256 amountInMaximum;
        uint160 sqrtPriceLimitX96;
    }

    function exactOutputSingle(ExactOutputSingleParams calldata params)
    external
    payable
    returns (uint256 amountIn);

    struct ExactOutputParams {
        bytes path;
        address recipient;
        // uint256 deadline;
        uint256 amountOut;
        uint256 amountInMaximum;
    }

    function exactOutput(ExactOutputParams calldata params)
    external
    payable
    returns (uint256 amountIn);
}

interface ISwapRouter {
    struct ExactInputSingleParams {
        address tokenIn;
        address tokenOut;
        uint24 fee;
        address recipient;
        uint256 deadline;
        uint256 amountIn;
        uint256 amountOutMinimum;
        uint160 sqrtPriceLimitX96;
    }

    function exactInputSingle(ExactInputSingleParams calldata params)
    external
    payable
    returns (uint256 amountOut);

    struct ExactInputParams {
        bytes path;
        address recipient;
        uint256 deadline;
        uint256 amountIn;
        uint256 amountOutMinimum;
    }

    function exactInput(ExactInputParams calldata params)
    external
    payable
    returns (uint256 amountOut);

    struct ExactOutputSingleParams {
        address tokenIn;
        address tokenOut;
        uint24 fee;
        address recipient;
        uint256 deadline;
        uint256 amountOut;
        uint256 amountInMaximum;
        uint160 sqrtPriceLimitX96;
    }

    function exactOutputSingle(ExactOutputSingleParams calldata params)
    external
    payable
    returns (uint256 amountIn);

    struct ExactOutputParams {
        bytes path;
        address recipient;
        uint256 deadline;
        uint256 amountOut;
        uint256 amountInMaximum;
    }

    function exactOutput(ExactOutputParams calldata params)
    external
    payable
    returns (uint256 amountIn);
}

contract LackDeadlineForUniswap {
    ISwapRouter public swapRouter;
    ISwapRouterBad public swapRouterBad;

    function bad() external {
        ISwapRouterBad.ExactInputSingleParams memory params1 = ISwapRouterBad
            .ExactInputSingleParams({
            tokenIn: address(0),
            tokenOut: address(0),
            fee: 0,
            recipient: address(this),
            amountIn: 0,
            amountOutMinimum: 0,
            sqrtPriceLimitX96: 0
        });
        swapRouterBad.exactInputSingle(params1);

        ISwapRouterBad.ExactInputParams memory params2 = ISwapRouterBad
            .ExactInputParams({
            path: "",
            recipient: address(0),
            amountIn: 0,
            amountOutMinimum: 0
        });
        swapRouterBad.exactInput(params2);

        ISwapRouterBad.ExactOutputSingleParams memory params3 = ISwapRouterBad
            .ExactOutputSingleParams({
            tokenIn: address(0),
            tokenOut: address(0),
            fee: 0,
            recipient: address(0),
        // uint256 deadline;
            amountOut: 0,
            amountInMaximum: 0,
            sqrtPriceLimitX96: 0
        });
        swapRouterBad.exactOutputSingle(params3);

        ISwapRouterBad.ExactOutputParams memory params4 = ISwapRouterBad
            .ExactOutputParams({
            path: "",
            recipient: address(0),
        // uint256 deadline;
            amountOut: 0,
            amountInMaximum: 0
        });
        swapRouterBad.exactOutput(params4);
    }

    function good() external {
        ISwapRouter.ExactInputSingleParams memory params1 = ISwapRouter
            .ExactInputSingleParams({
            tokenIn: address(0),
            tokenOut: address(0),
            fee: 0,
            recipient: address(this),
            deadline: block.timestamp,
            amountIn: 0,
            amountOutMinimum: 0,
            sqrtPriceLimitX96: 0
        });
        swapRouter.exactInputSingle(params1);

        ISwapRouter.ExactInputParams memory params2 = ISwapRouter
            .ExactInputParams({
            path: "",
            recipient: address(0),
            deadline: block.timestamp,
            amountIn: 0,
            amountOutMinimum: 0
        });
        swapRouter.exactInput(params2);

        ISwapRouter.ExactOutputSingleParams memory params3 = ISwapRouter
            .ExactOutputSingleParams({
            tokenIn: address(0),
            tokenOut: address(0),
            fee: 0,
            recipient: address(0),
            deadline: block.timestamp,
            amountOut: 0,
            amountInMaximum: 0,
            sqrtPriceLimitX96: 0
        });
        swapRouter.exactOutputSingle(params3);

        ISwapRouter.ExactOutputParams memory params4 = ISwapRouter
            .ExactOutputParams({
            path: "",
            recipient: address(0),
            deadline: block.timestamp,
            amountOut: 0,
            amountInMaximum: 0
        });
        swapRouter.exactOutput(params4);
    }
}
