# Bitcoin Wallet Alert

Python script to monitor a Bitcoin wallet and send alerts via Telegram.

## Setup

1. Create an .env file with the Telegram bot or chat information
```
TELEGRAM_CHAT=<your-telegram-chat-id>
TELEGRAM_TOKEN=<your-telegram-token>
```
2. Install the Python3 requirements
```
sudo pip3 install -r requirements.txt
```
## Usage
```
usage: btc_wallet_alert.py [-h] --wallet WALLET [--telegram-notify]
                           [--time [TIME]]

Bitcoin Wallet Alert

optional arguments:
  -h, --help         show this help message and exit
  --wallet WALLET    wallet address to check
  --telegram-notify  send a telegram notification
  --time [TIME]      time in seconds between successive check (default: 60)
```