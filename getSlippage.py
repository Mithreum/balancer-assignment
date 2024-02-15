import requests
import json


def encode_data(contract_address, function_signature, pool_id, kind, token_a, token_b, amount, sender, data_feed_a, data_feed_b):
    '''Converts the input params to an Ethereum API request body'''
    return {
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [
            {
                "to": contract_address,
                "data": function_signature + pool_id[2:] + kind[2:] + token_a[2:] + token_b[2:] + amount[2:] + sender[2:] + data_feed_a[2:] + data_feed_b[2:]
            },
            "latest"],
        "id": 1
    }


def get_abi():
    '''
    May be required if called with web3.py
    Returns the ABI or throws an error: 'ABI file not found
    '''

    with open ('./artifacts/contracts/SlippageRequester.sol/SlippageRequester.json', 'r') as file:

        json_data = file.read()

        data_dict = json.loads(json_data)

        if(data_dict and data_dict['abi']):
            return data_dict['abi']
        else:
            raise RuntimeError("ABI file not found")


# 1. Populate the request variables:
ethereum_node_url   = "https://rpc.vnet.tenderly.co/devnet/my-first-devnet/eaf20206-5ec4-4835-a21c-82541136d115" # https://chainlist.org/
contract_address    = "0x123456..." # Replace with the actual contract address
function_signature  = "0x3087bfd8"  # Function signature
pool_id             = "0x01.."  # Replace with the actual bytes32 value of the pool ID
kind                = "0x00"  # Assuming GIVEN_IN is represented by 0 & GIVEN_OUT by 1 (0x01)
token_a             = "0x123..."  # Replace with the actual address of tokenA
token_b             = "0x456..."  # Replace with the actual address of tokenB
amount              = str(hex(1_000_000 * 1e18)) # Assuming 18 decimals for the token amount
sender              = "0x738b2B2153d78Fc8E690b160a6fC919B2C88b6A4"  # Or replace with the actual sender's address
data_feed_a         = "0xabc..."  # Replace with the actual address of Chainlink data feed for token A
data_feed_b         = "0xdef..."  # Replace with the actual address of Chainlink data feed for token B

# 2. Prepare the data
request_data = encode_data(contract_address, function_signature, pool_id, kind, token_a, token_b, amount, sender, data_feed_a, data_feed_b)

# 3. Execute the request
response = requests.post(ethereum_node_url, json=request_data)

# 4. Parse the response
result = json.loads(response.text)['result']

# 5. Convert hex result to integer
tup_result = int(result[0], 16), int(result[1], 16), int(result[2], 16)

# 6. Output the result (NB. divide each token by 10 ** decimals)
print("Price of A", tup_result[0], "Price of B", tup_result[1], "Slippage:", tup_result[2])