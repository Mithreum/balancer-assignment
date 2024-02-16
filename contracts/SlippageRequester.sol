// Original license: SPDX_License_Identifier: GPL-3.0-or-later
pragma solidity >=0.7.0;

import { IVault } from "./interfaces/IVault.sol";
import { IAsset } from "./interfaces/IAsset.sol";
import { AggregatorV3Interface } from "./interfaces/AggregatorV3Interface.sol";

contract SlipageRequester {
    address public balancerAddress;

    constructor() {
        balancerAddress = address(0xE39B5e3B6D74016b2F6A9673D7d7493B6DF549d5);
    }

    /**
    * @dev Fetches the ChainLink token price
    * @param dataFeed_ the address of the Chainlink data feed
    * @return the token price 
    *
    * https://docs.chain.link/data-feeds/price-feeds/addresses?network=ethereum&page=1
    */
    function getChainlinkPrice(address dataFeed_)
        external
        view
        returns (int256)
    {
        return _getChainlinkPrice(dataFeed_);
    }

    /**
     * @dev Utility returning the token selector for `getChainlinkPrice`
     */
    function getChainLinkPriceselector() external pure returns (bytes4) {
        return this.getChainlinkPrice.selector;
    }

    /**
     * @dev Utility returning the token selector for `getSlippage`
     */
    function getFunctionSelector() external pure returns (bytes4) {
        return this.getSlippage.selector;
    }

    /**
     * @dev Utility returning the token selector for `getSwapValue`
     */
    function getSwapValueSelector() external pure returns (bytes4){
        return this.getSwapValue.selector;
    }

    /**
     * @dev Fetches the slippage
     * @param poolId_ the unique identifier of the requested token pool
     * @param kind_ ∈ {GIVEN_IN, GIVEN_OUT} = uint8 {0x00, 0x01}
     * @param tokenA_ the address of the firs token in the pair
     * @param tokenB_ the address of the second token
     * @param amount_ the sum x token decimals
     * @param sender_ a valid EOA's address
     * @param dataFeedA_ the address of the Chainlink data feed for token A
     * @param dataFeedB_ the address of the Chainlink data feed for token B
     * @return tuple (tokenA in USD, tokenB in USD, slippage in USD, decimalsA, decimalsB)
     */
    function getSlippage(
        bytes32 poolId_,
        IVault.SwapKind kind_,
        address tokenA_,
        address tokenB_,
        uint256 amount_,
        address sender_,
        address dataFeedA_,
        address dataFeedB_
    )
        external
        returns (
            uint256,
            uint256,
            int256,
            uint8,
            uint8
        )
    {
        // 1. Get the estimation from the swap dry run
        uint256 returnValue = _getSwapValue(
            poolId_,
            kind_,
            tokenA_,
            tokenB_,
            amount_,
            sender_
        );

        // 2. Get the token prices
        int256 tokenAPrice = _getChainlinkPrice(dataFeedA_);
        int256 tokenBPrice = _getChainlinkPrice(dataFeedB_);

        // 3. Calculate the expected and observed values in USD
        uint256 expected = (amount_ * uint256(tokenAPrice)) /
            (10**AggregatorV3Interface(dataFeedA_).decimals());
        uint256 actual = (returnValue * uint256(tokenBPrice)) /
            (10**AggregatorV3Interface(dataFeedB_).decimals());

        // 4. Return the values
        return (
            uint256(tokenAPrice) * amount_, // Token A in USD
            uint256(tokenBPrice) * returnValue, // Token B in USD
            int256(actual) - int256(expected), // Slippage in USD
            AggregatorV3Interface(dataFeedA_).decimals(),
            AggregatorV3Interface(dataFeedB_).decimals()
        );
    }

    /**
     * @dev Querries the Balancer contract
     * @param poolId_ the unique identifier of the requested token pool
     * @param kind_ ∈ {GIVEN_IN, GIVEN_OUT}
     * @param tokenA_ the address of the firs token in the pair
     * @param tokenB_ the address of the second token
     * @param amount_ the sum x token decimals
     * @param sender_ a valid EOA's address
     * @return the value of token B swapped for token A
     */
    function getSwapValue(
        bytes32 poolId_,
        IVault.SwapKind kind_,
        address tokenA_,
        address tokenB_,
        uint256 amount_,
        address sender_
    ) external returns (uint256) {
        return
            _getSwapValue(poolId_, kind_, tokenA_, tokenB_, amount_, sender_);
    }

    /**
     * @dev Retrievs the token price from the ChainLink Oracle
     * @param dataFeed_ the address of the token price feed
     * @return the current token price in USD
     */
    function _getChainlinkPrice(address dataFeed_)
        private
        view
        returns (int256)
    {
        (
            ,
            /* uint80 roundID */
            int256 answer,   
            , /*uint startedAt*/
            , /*uint timeStamp*/
            /*uint80 answeredInRound*/
        ) = AggregatorV3Interface(dataFeed_).latestRoundData();

        return answer;
    }

    function _getSwapValue(
        bytes32 poolId_,
        IVault.SwapKind kind_,
        address tokenA_,
        address tokenB_,
        uint256 amount_,
        address sender_
    ) private returns (uint256) {
        // 1. Populate param singleSwap
        IVault.SingleSwap memory singleSwap = IVault.SingleSwap({
            poolId: poolId_,
            kind: kind_,
            assetIn: IAsset(address(tokenA_)),
            assetOut: IAsset(address(tokenB_)),
            amount: amount_,
            userData: bytes("")
        });
        // 2. Populate param funds
        IVault.FundManagement memory funds = IVault.FundManagement({
            sender: sender_,
            fromInternalBalance: false,
            recipient: payable(address(0)),
            toInternalBalance: false
        });

        // 3. Prepare the function call data
        bytes memory data = abi.encodeWithSelector(
            bytes4(
                keccak256(
                    "querySwap((bytes32,uint8,address,address,uint256,bytes),(address,bool,address,bool))"
                )
            ),
            singleSwap,
            funds
        );

        // 4. Execute the function call using .call()
        (bool success, bytes memory returnData) = balancerAddress.call(data);
        require(success, "Function call failed");

        // 5. Decode from bytes32 to uint256
        uint256 returnValue;
        assembly {
            returnValue := mload(add(returnData, 32))
        }

        // 6. return the value
        return returnValue;
    }
}

