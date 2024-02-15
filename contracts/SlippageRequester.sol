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
     * @dev Fetches the slippage
     * @param poolId_ the unique identifier of the requested token pool
     * @param kind_ ∈ {GIVEN_IN, GIVEN_OUT}
     * @param tokenA_ the address of the firs token in the pair
     * @param tokenB_ the address of the second token
     * @param amount_ the sum x token decimals
     * @param sender_ a valid EOA's address
     * @param dataFeedA_ the address of the Chainlink data feed for token A
     * @param dataFeedB_ the address of the Chainlink data feed for token B
     * @return tuple (tokenA in USD, tokenB in USD, slippage in USD)
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
            int256
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
            uint256(tokenAPrice) * amount_,     // Token A in USD
            uint256(tokenBPrice) * returnValue, // Token B in USD
            int256(actual) - int256(expected)   // Slippage in USD
        );
    }

    /**
    * @dev Utility returning the token selector for `getSlippage`
    */
    function calculateFunctionSelector() external pure returns (bytes4) {
        return this.getSlippage.selector;
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
            /* uint80 roundID */,
            int answer,
            /*uint startedAt*/,
            /*uint timeStamp*/,
            /*uint80 answeredInRound*/

        ) = AggregatorV3Interface(dataFeed_).latestRoundData();

        return answer;
    }

    /**
    * @dev Populates the SingleSwap struct
    */
    function _populateSingleSwap(
        bytes32 poolId_,
        IVault.SwapKind kind_,
        address tokenA_,
        address tokenB_,
        uint256 amount_
    ) private pure returns (IVault.SingleSwap memory) {
        return
            IVault.SingleSwap({
                poolId: poolId_,
                kind: kind_,
                assetIn: IAsset(tokenA_),
                assetOut: IAsset(tokenB_),
                amount: amount_,
                userData: bytes("")
            });
    }

    /**
    * @dev Populates the FundManagement struct
    * @param sender_ a valid EVM EOA
    */
    function _populateFundManagement(address sender_)
        private
        pure
        returns (IVault.FundManagement memory)
    {
        return
            IVault.FundManagement({
                sender: sender_,
                fromInternalBalance: false, // ignored
                recipient: payable(sender_),
                toInternalBalance: true // ignored
            });
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
    function _getSwapValue(
        bytes32 poolId_,
        IVault.SwapKind kind_,
        address tokenA_,
        address tokenB_,
        uint256 amount_,
        address sender_
    ) private returns (uint256) {
        // 1. Call querySwap with params
        bytes memory callData = abi.encodeWithSignature(
            "querySwap((bytes32, uint8, address, address, uint256, bytes),(address, bool, address, bool))",
            _populateSingleSwap(poolId_, kind_, tokenA_, tokenB_, amount_),
            _populateFundManagement(sender_)
        );

        // 2. Call the Balancer contract
        (bool success, bytes memory data) = balancerAddress.call(callData);

        // 3. Check success or revert
        require(success, "Call failed");

        // 4. Convert the return value to uint256
        uint256 returnValue;
        assembly {
            returnValue := mload(add(data, 32))
        }

        // 5. Return the value of token B
        return returnValue;
    }
}
