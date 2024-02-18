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
                "data": function_signature 
                + pool_id[2:] 
                + format(int(kind, 16), '064x')
                + token_a[2:].rjust(64, '0')
                + token_b[2:].rjust(64, '0')
                + format(amount, '064x')
                + sender[2:].rjust(64, '0')
                + data_feed_a[2:].rjust(64, '0')
                + data_feed_b[2:].rjust(64, '0')
            },
            "latest"],
        "id": 1
    }


def get_slippage(url, data) -> tuple:
    '''Querries the contract & parses its output'''

    # 1. Execute the request
    response = requests.post(url, json=data)

    # 2. Parse the response
    result_hex = json.loads(response.text)['result']

    # 3. Parse the hexadecimal string into respective components
    token_a_price = int(result_hex[2:66], 16)
    token_b_price = int(result_hex[66:130], 16)
    # contract_slippage = int(result_hex[130:194], 16) # Ignore
    token_a_price_decimals = int(result_hex[194:258], 16)
    token_b_price_decimals = int(result_hex[258:], 16)

    token_a_decimals = 6
    token_b_decimals = 18

    expected = token_a_price / 10 ** (token_a_price_decimals + token_a_decimals)
    actual = token_b_price / 10 ** (token_b_price_decimals + token_b_decimals)
    slippage = expected - actual
    slip_percent = slippage / expected * 100

    return expected, actual, slippage, slip_percent


# TESTS:

# 1. Populate the request variables:
ethereum_node_url   = "https://polygon.drpc.org" # https://chainlist.org/
contract_address    = "0x0A6A1Beb7b0b3545578818f45f4e6219615d25aD" # Polygon, Replace with the actual contract address on other chains
function_signature  = "0x3087bfd8"  # Function signature
pool_id             = "0x0297e37f1873d2dab4487aa67cd56b58e2f27875000100000000000000000002"  # Replace with the actual bytes32 value of the pool ID
kind                = "0x00"  # Assuming GIVEN_IN is represented by 0 & GIVEN_OUT by 1 (0x01)
token_a             = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"  # USDC.e or Replace with the actual address of tokenA
token_b             = "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"  # WMATIC or Replace with the actual address of tokenB
amount              = 1_000_000_000
sender              = "0x8cE9Edd9FeE8bEbbF33d059602Fbd487fdEB3661"  # any valid EVM address
data_feed_a         = "0xfE4A8cc5b5B2366C1B58Bea3858e81843581b2F7"  # USDC/USD Replace with the actual address of Chainlink data feed for token A
data_feed_b         = "0xAB594600376Ec9fD91F8e885dADF0CE036862dE0"  # MATIC/USD Replace with the actual address of Chainlink data feed for token B

# 2. Prepare the data
request_data = encode_data(contract_address, function_signature, pool_id, kind, token_a, token_b, amount, sender, data_feed_a, data_feed_b)

# 3. 
[expected, actual, slippage, slip_percent] = get_slippage(ethereum_node_url, request_data)

# 4. Output the result (NB. divide each token by 10 ** decimals)
print("USDC / WMATIC\n Expected($):\t", expected, '\n', "Actual  ($):\t", actual, '\n', "Slippage($):\t", slippage, '\n', f"Slippage(%): \t{" {:.2f}%".format(slip_percent)}")
