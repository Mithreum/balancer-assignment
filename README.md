# Sample Assignment

## Usage

1. Deploy the contract on the required EVM chain
2. Populate the variables with the relevant data for tokens A & B
3. Run the script


## Deployd contracts:

[Polygon](https://polygonscan.com/address/0x0a6a1beb7b0b3545578818f45f4e6219615d25ad)

## Testing

1. Install the required dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests
```

2. Replace the variables with the required values

3. Run the script

```bash
python3 getSlippage.py
```

Response example: for USDC / WMATIC, amount 1_000_000_000

```bash
USDC / WMATIC
 Expected($):    1000.02998 
 Actual  ($):    993.344667370729 
 Slippage($):    6.6853126292710385 
 Slippage(%):    0.67%
```

## Deployed contracts

[Gnosis](https://gnosisscan.io/address/0x6b30f76cece9f92d27f0e9ad78312e77709e74a5#code)
[Ethereum](https://etherscan.io/address/0x6b30f76CecE9F92D27f0e9Ad78312E77709E74A5#code)
[Polygon](https://polygonscan.com/address/0x0a6a1beb7b0b3545578818f45f4e6219615d25ad#code)
