# Python Indodax API Wrapper

This project provides a Python wrapper for interacting with the Indodax API. It includes classes for managing API keys, fetching trade history, and converting data to CSV format.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/glenkusuma/python-indodax-api-wrapper.git
    ```

2. Navigate to the project directory:

    ```bash
    cd python-indodax-api-wrapper
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Set up your API keys by creating a `.env` file based on the `.env.example` provided.
2. Use the classes provided in the project to interact with the Indodax API.

Example usage:

```python
from indodax import Indodax
from apikeymanager import ApiKeyManager
from dataparser import DataParser

# Get API keys
api_key, secret_key_bytes = ApiKeyManager().get_api_keys()

# Initialize Indodax account
account = Indodax(api_key, secret_key_bytes)

# Fetch trade history for a specific coin
COIN = 'vra'
trade_history = account.trade_history(COIN)

# Convert trade history to CSV format
OUTPUT_FOLDER = 'output'
DataParser().trade_history.json_to_csv(trade_history, OUTPUT_FOLDER)
```

## Folder Structure

```txt
python-indodax-api-wrapper/
├─ .gitignore
├─ .env.example
├─ apikeymanager.py
├─ dataparser.py
├─ indodax.py
├─ price.py
├─ trade_history.ipynb
└─ output/
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with any enhancements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
