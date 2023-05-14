from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3
from zksync2.core.types import Token, EthBlockParams
from zksync2.module.module_builder import ZkSyncBuilder
from zksync2.provider.eth_provider import EthereumProvider

from termcolor import cprint
import time
import random
from tqdm import tqdm
from loguru import logger
import telebot

# PRC провайдеры
ZKSYNC_URL = "https://mainnet.era.zksync.io"
ETH_URL = "https://rpc.ankr.com/eth"
# ZKSYNC_URL = "https://zksync2-testnet.zksync.dev"
# ETH_URL = "https://rpc.ankr.com/eth_goerli"

# Кол-во ETH для отправки, значение рандомно выберется между MIN_AMOUNT и MAX_AMOUNT.
MIN_AMOUNT = 0.001
MAX_AMOUNT = 0.003

# Значение GWEI при котором совершится транзакция, иначе будет ждать.
# Если значение пустое, то будет использован текущий GWEI сети
GWEI = 21

# Пауза выполения скрипта между кошельками (рандомно между SLEEP_TIME_MIN и SLEEP_TIME_MAX)
SLEEP_TIME_MIN = 300
SLEEP_TIME_MAX = 900

# настройка отправки результатов в тг бота
TG_BOT_SEND = False # True / False. Если True, тогда будет отправлять результаты
TG_TOKEN    = '' # токен от тг-бота
TG_ID       = 000000000 # id твоего телеграмма, узнать его можно здесь : https://t.me/getmyid_bot

STR_DONE    = '✅ ' 
STR_CANCEL  = '❌ '

list_send = []
def send_msg():

    try:
        str_send = '\n'.join(list_send)
        bot = telebot.TeleBot(TG_TOKEN)
        bot.send_message(TG_ID, str_send, parse_mode='html')  

    except Exception as error: 
        logger.error(error)

def sleeping(from_sleep, to_sleep):

    x = random.randint(from_sleep, to_sleep)
    for i in tqdm(range(x), desc='sleep ', bar_format='{desc}: {n_fmt}/{total_fmt}'):
        time.sleep(1)