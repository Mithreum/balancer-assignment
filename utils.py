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

def parse_signed_number(hex_string: str, num_bytes: int) -> int:
    # Convert hexadecimal string to an integer
    value = int(hex_string, 16)
    
    # Check if the most significant bit is set (indicating a negative number)
    if value & (1 << (num_bytes * 8 - 1)):
        # Convert the value to a negative number using two's complement
        value -= 1 << (num_bytes * 8)

    return value


def get_slippage(url, data, token_a_decimals, token_b_decimals) -> tuple:
    '''Querries the contract & parses its output'''

    try:

        # 1. Execute the request
        response = requests.post(url, json=data)

        # 2. Parse the response
        result_hex = json.loads(response.text)['result']

        # print('result_hex', result_hex)

        # 3. Parse the hexadecimal string into respective components
        step = 64 # 32 bytes * 2 chars representation
        start = 2 # 0x prefix
        stop = start + step
        slippage_percent = parse_signed_number(result_hex[start:stop], 32)
        start = stop
        stop += step
        contract_slippage = parse_signed_number(result_hex[start:stop], 32)
        start = stop
        stop += step
        token_a_price = int(result_hex[start:stop], 16)
        start = stop
        stop += step
        token_b_price = int(result_hex[start:stop], 16)

        return slippage_percent / 10 ** (6), contract_slippage / 10 ** (6), token_a_price / 10 ** (token_a_decimals + 8), token_b_price / 10 ** (token_b_decimals + 8)

    except:
        print('Check the RPC URL, pool_id, contract or feed addresses')
        return 'error', 'error', 'error', 'error'
    
def main(tests):

    for test in tests:

        try:

            # 1. Prepare the data
            request_data = encode_data(test['contract'], test['function'], test['pool_id'], test['kind'], test['token_a'], test['token_b'], test['amount'], test['sender'], test['feed_a'], test['feed_b'])

            # print('request_data', request_data)

            # 2. 
            [slippage_percent, contract_slippage, token_a_price, token_b_price] = get_slippage(test['rpc_url'], request_data, test['a_decimals'], test['b_decimals'])

            # 3. Output the result (NB. divide each token by 10 ** decimals)
            print(f"{test['pair']}\n Slippage %:\t", slippage_percent, '\n', "Slippage (V):\t", contract_slippage, '\n', "Price A($):\t", token_a_price, '\n', "Price B($): \t", token_b_price)

        except Exception as e:
            print('An error occured', e)