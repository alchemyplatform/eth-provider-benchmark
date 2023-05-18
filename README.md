# Benchmark of Ethereum Service Providers

This benchmark allows you to compare the accuracy and consistency of Ethereum service providers, including Alchemy, Infura and CloudFlare, head to head on a suite of tests.

## Installation

Be sure you have the latest version of [Python3](https://www.python.org/downloads/), then activate a virtual environment with the needed dependencies by running:

```bash
bash setup.sh
source env/bin/activate
```

## Usage

To see the paramaters needed to invoke the tests, use:

```bash
python3 provider_benchmark.py -h
```

### Log Consistency

```bash
python3 provider_benchmark.py -i <<INFURA_API_KEY>> -a <<ALCHEMY_API_KEY>> -c -mainnet -http --log_consistency
```

```bash
python3 provider_benchmark.py -i <<INFURA_API_KEY>> -a <<ALCHEMY_API_KEY>> -c -sepolia -ws --log_consistency
```

### Log Accuracy

```bash
python3 provider_benchmark.py -i <<INFURA_API_KEY>> -a <<ALCHEMY_API_KEY>> -c -mainnet -http --pending_transactions
```

```bash
python3 provider_benchmark.py -i <<INFURA_API_KEY>> -a <<ALCHEMY_API_KEY>> -c -sepolia -ws --pending_transactions
```

### Config

Each test that you run is repeated 457 times, with a 5 second delay, but you can edit these parameters in [config.py](config.py).

## Contributing

We are constantly working on adding new tests, so stay tuned for updates! Feel free to add more extensive tests and other providers as you see fit.
