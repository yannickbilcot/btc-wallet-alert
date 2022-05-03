#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Yannick BILCOT
# Date created: 03/04/2021
# =============================================================================
"""BTC Wallet Alert"""
# =============================================================================
import requests
from bs4 import BeautifulSoup
import argparse
import logging
import os
import sys
import time
from dotenv import load_dotenv


def send_telegram_msg(message: str):
    '''
    Send a Telegram message
        Parameters:
            message (str): text message to send (with Markdownv2 syntax)
    '''
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}'
    try:
        r = requests.post(f'{url}/sendMessage', data={'chat_id': TELEGRAM_CHAT,
                'text': message, 'parse_mode': 'MarkdownV2', 'disable_web_page_preview': 'true'})
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        logging.error(f"Send telegram msg: {errh}")


def check_wallet(wallet: str, period: int = 60, telegram_notify: bool = False):
    '''
    Check a bitcoin wallet transactions change
        Parameters:
            wallet (str): BTC wallet address
            period (int): time in seconds between successive check
            telegram_notify (bool): send a telegram msg when a change is detected
    '''
    # target URL
    url = f"https://www.blockchain.com/btc/address/{wallet}"

    # act like a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                      '(HTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    prev_transactions_number = ""
    first_run = True

    while True:
        # download the page
        response = requests.get(url, headers=headers)
        # parse the downloaded homepage
        soup = BeautifulSoup(response.text, "html.parser")

        # get the transactions number
        for script in soup(["script", "style"]):
            script.extract()
        page_text = soup.get_text().split()
        index = page_text.index("transacted") + 1
        transactions_number = page_text[index]

        # get the last transaction amount
        soup_transaction = soup.select_one('div[direction="vertical"] > div > div:last-of-type')
        last_transaction_amount = soup_transaction.select('span')[-1].get_text()
        
        # get the last transaction date
        soup_transaction = soup.select_one('div[direction="vertical"] > div:nth-of-type(2)')
        last_transaction_date = soup_transaction('span')[-1].get_text()

        # compare the number of transactions with the previous version
        if prev_transactions_number != transactions_number:
            prev_transactions_number = transactions_number
            if first_run:
                first_run = False
                logging.info(f"+-+-+-+-+ Start Monitoring +-+-+-+-+")
                logging.info(f"Wallet: {wallet}")
                logging.info(f"URL: {url}")
                logging.info(f"Original number of transactions: {transactions_number}")
                logging.info(f"Last transaction was: {last_transaction_amount} ({last_transaction_date})")
                if telegram_notify:
                    send_telegram_msg(f"""Start monitoring of Bitcoin wallet [{wallet[0:8]}]({url})
Last transaction: `{last_transaction_amount} ({last_transaction_date})`""")

            else:
                logging.info(f"+-+-+-+-+ Changes detected +-+-+-+-+")
                logging.info(f"New number of transactions: {transactions_number}")
                logging.info(f"The wallet changed by: {last_transaction_amount}")
                if telegram_notify:
                    send_telegram_msg(f"The wallet [{wallet[0:8]}]({url}) changed by `{last_transaction_amount}`")
        else:
            logging.debug("No changes")
        time.sleep(period)
        continue


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bitcoin Wallet Alert')
    parser.add_argument("--wallet", required=True, help="wallet address to check")
    parser.add_argument("--telegram-notify", action="store_true", help="send a telegram notification")
    parser.add_argument('--time', nargs="?", const=1, default=60, type=int, help="time in seconds between successive check (default: 60 seconds)")
    args = parser.parse_args()

    log_handler = [logging.StreamHandler()]
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
#       logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ])
    
    wdir = sys.path[0]
    load_dotenv(f'{wdir}/.env')
    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
    TELEGRAM_CHAT = os.environ.get('TELEGRAM_CHAT')

    check_wallet(args.wallet, args.time, args.telegram_notify)
