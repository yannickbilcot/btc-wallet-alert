# Bitcoin Wallet Alert

Python script to monitor a Bitcoin wallet and send alerts to Discord and/or Telegram.

## Setup

1. Install the Python3 requirements
```
sudo pip3 install -r requirements.txt
```

2. Create an .env file with the Discord and/or Telegram chat information
```
TELEGRAM_CHAT=<your-telegram-chat-id>
TELEGRAM_TOKEN=<your-telegram-token>
DISCORD_WEBHOOK_URL=<your-discord-webhook-url>
```
## Usage
```
usage: btc_wallet_alert.py [-h] --wallet WALLET [--telegram-notify]
                           [--discord-notify] [--time [TIME]] [--debug]

Bitcoin Wallet Alert

optional arguments:
  -h, --help         show this help message and exit
  --wallet WALLET    wallet address to check
  --telegram-notify  send a telegram notification
  --discord-notify   send a discord notification
  --time [TIME]      time in seconds between successive check (default: 60
                     seconds)
  --debug            enable debug level logging
```
