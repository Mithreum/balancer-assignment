// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FunctionSelectorCalculator {
    function calculateFunctionSelector(string memory functionName) external pure returns (bytes4) {
        return bytes4(keccak256(abi.encodePacked(functionName)));
    }
}