import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import ccxt
import pandas as pd
import ta
import requests
import time
from datetime import datetime

BOT_TOKEN = os.environ.get("8870951691:AAHCKTNEr22bxn2hMk_YAjPIenPvQ8bdUUw")
CHANNEL_ID = os.environ.get("4326423360")

TIMEFRAME = "15m"

SYMBOLS = [
    "BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "XRP/USDT",
    "ADA/USDT", "DOGE/USDT", "AVAX/USDT", "DOT/USDT", "LINK/USDT",
    "TRX/USDT", "POL/USDT", "SHIB/USDT", "LTC/USDT", "UNI/USDT",
    "ATOM/USDT", "XLM/USDT", "NEAR/USDT", "APT/USDT", "SUI/USDT",
    "ARB/USDT", "OP/USDT", "INJ/USDT", "TIA/USDT", "FIL/USDT",
    "AAVE/USDT", "GRT/USDT", "PEPE/USDT", "QNT/USDT", "FET/USDT"
]

COIN_IMAGES = {
    "BTC/USDT": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png",
    "ETH/USDT": "https://assets.coingecko.com/coins/images/279/large/ethereum.png",
    "BNB/USDT": "https://assets.coingecko.com/coins/images/825/large/bnb-icon2_2x.png",
    "SOL/USDT": "https://assets.coingecko.com/coins/images/4128/large/solana.png",
    "XRP/USDT": "https://assets.coingecko.com/coins/images/44/large/xrp-symbol-white-128.png",
    "ADA/USDT": "https://assets.coingecko.com/coins/images/975/large/cardano.png",
    "DOGE/USDT": "https://assets.coingecko.com/coins/images/5/large/dogecoin.png",
    "AVAX/USDT": "https://assets.coingecko.com/coins/images/12559/large/Avalanche_Circle_RedWhite_Trans.png",
    "DOT/USDT": "https://assets.coingecko.com/coins/images/12171/large/polkadot.png",
    "LINK/USDT": "https://assets.coingecko.com/coins/images/877/large/chainlink-new-logo.png",
    "TRX/USDT": "https://assets.coingecko.com/coins/images/1094/large/tron-logo.png",
    "SHIB/USDT": "https://assets.coingecko.com/coins/images/11939/large/shib.png",
    "LTC/USDT": "https://assets.coingecko.com/coins/images/2/large/litecoin.png",
    "UNI/USDT": "https://assets.coingecko.com/coins/images/12504/large/uniswap.png",
    "ATOM/USDT": "https://assets.coingecko.com/coins/images/1481/large/cosmos_hub.png",
    "XLM/USDT": "https://assets.coingecko.com/coins/images/100/large/Stellar_lumens.png",
    "NEAR/USDT": "https://assets.coingecko.com/coins/images/10365/large/near.jpg",
    "APT/USDT": "https://assets.coingecko.com/coins/images/26455/large/aptos_round.png",
    "SUI/USDT": "https://assets.coingecko.com/coins/images/26340/large/Sui_logo.png",
    "ARB/USDT": "https://assets.coingecko.com/coins/images/16547/large/photo_2023-03-29_21.47.00.jpeg",
    "OP/USDT": "https://assets.coingecko.com/coins/images/25244/large/Optimism.png",
    "INJ/USDT": "https://assets.coingecko.com/coins/images/12882/large/Secondary_Symbol.png",
    "FIL/USDT": "https://assets.coingecko.com/coins/images/12817/large/filecoin.png",
    "AAVE/USDT": "https://assets.coingecko.com/coins/images/12645/large/AAVE.png",
    "GRT/USDT": "https://assets.coingecko.com/coins/images/13397/large/Grt.png",
    "PEPE/USDT": "https://assets.coingecko.com/coins/images/29850/large/pepe-token.jpeg",
    "FET/USDT": "https://assets.coingecko.com/coins/images/11636/large/FET.png"
}
DEFAULT_IMAGE = "https://cdn-icons-png.flaticon.com/512/5968/5968339.png"

def send_crypto_signal(coin_name, direction, strategy, entry, leverage, tp1, tp2, sl, image_url):
    emoji = "🟢" if direction.lower() == "long" else "🔴"
    direction_text = "LONG" if direction.lower() == "long" else "SHORT"

    text = f"""
<b>{emoji} Automated Signal on {coin_name} {emoji}</b>
<i>Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}</i>
<b>Strategy:</b> <code>{strategy}</code>

━━━━━━━━━━━━━━━
<b>Direction:</b> <code>{direction_text}</code>
<b>Entry:</b> <code>{entry}</code>
<b>Leverage:</b> <code>{leverage}x</code>
━━━━━━━━━━━━━━━
<b>Target 1 (TP1):</b> <code>{tp1}</code>
<b>Target 2 (TP2):</b> <code>{tp2}</code>
<b>Stop Loss (SL):