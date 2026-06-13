import os
import ssl
# Fix for GitHub SSL Connection issues with Binance
ssl._create_default_https_context = ssl._create_unverified_context

import ccxt
import pandas as pd
import requests
import time
from datetime import datetime

BOT_TOKEN = os.environ.get("8870951691:AAHCKTNEr22bxn2hMk_YAjPIenPvQ8bdUUw")
CHANNEL_ID = os.environ.get("4326423360")

TIMEFRAME = "1h"

SYMBOLS = [
    "BTC/USDT",
    "ETH/USDT",
    "SOL/USDT",
    "BNB/USDT",
    "XRP/USDT",
    "DOGE/USDT"
]

COIN_IMAGES = {
    "BTC/USDT": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png",
    "ETH/USDT": "https://assets.coingecko.com/coins/images/279/large/ethereum.png",
    "SOL/USDT": "https://assets.coingecko.com/coins/images/4128/large/solana.png",
    "BNB/USDT": "https://assets.coingecko.com/coins/images/825/large/bnb-icon2_2x.png",
    "XRP/USDT": "https://assets.coingecko.com/coins/images/44/large/xrp-symbol-white-128.png",
    "DOGE/USDT": "https://assets.coingecko.com/coins/images/5/large/dogecoin.png"
}
DEFAULT_IMAGE = "https://cdn-icons-png.flaticon.com/512/5968/5968339.png"

def send_crypto_signal(coin_name, direction, entry, leverage, tp1, tp2, sl, image_url):
    emoji = "🟢" if direction.lower() == "long" else "🔴"
    direction_text = "LONG" if direction.lower() == "long" else "SHORT"

    text = f"""
<b>{emoji} Automated Signal on {coin_name} {emoji}</b>
<i>Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}</i>

━━━━━━━━━━━━━━━
<b>Direction:</b> <code>{direction_text}</code>
<b>Entry:</b> <code>{entry}</code>
<b>Leverage:</b> <code>{leverage}x</code>
━━━━━━━━━━━━━━━
<b>Target 1 (TP1):</b> <code>{tp1}</code>
<b>Target 2 (TP2):</b> <code>{tp2}</code>
<b>Stop Loss (SL):</b> <code>{sl}</code>
━━━━━━━━━━━━━━━
<i>Automated signal based on EMA Crossover. Trade responsibly.</i>
    """

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    payload = {
        "chat_id": CHANNEL_ID,
        "photo": image_url,
        "caption": text,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload)
        print(f"Signal sent for {coin_name}")
    except Exception as e:
        print(f"Error sending {coin_name} signal: {e}")

def analyze_and_trade():
    print("Starting market scan...")
    exchange = ccxt.binance()
    
    for symbol in SYMBOLS:
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, TIMEFRAME, limit=50)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['ema_9'] = df['close'].ewm(span=9, adjust=False).mean()
            df['ema_21'] = df['close'].ewm(span=21, adjust=False).mean()
            
            current_close = df['close'].iloc[-1]
            curr_ema9 = df['ema_9'].iloc[-1]
            curr_ema21 = df['ema_21'].iloc[-1]
            prev_ema9 = df['ema_9'].iloc[-2]
            prev_ema21 = df['ema_21'].iloc[-2]
            
            img = COIN_IMAGES.get(symbol, DEFAULT_IMAGE)

            if prev_ema9 < prev_ema21 and curr_ema9 > curr_ema21:
                print(f"BUY SIGNAL on {symbol}!")
                entry = round(current_close, 2)
                tp1 = round(entry * 1.015, 2)
                tp2 = round(entry * 1.03, 2)
                sl = round(entry * 0.985, 2)
                send_crypto_signal(symbol, "LONG", str(entry), "10", str(tp1), str(tp2), str(sl), img)
                time.sleep(2)
                
            elif prev_ema9 > prev_ema21 and curr_ema9 < curr_ema21:
                print(f"SELL SIGNAL on {symbol}!")
                entry = round(current_close, 2)
                tp1 = round(entry * 0.985, 2)
                tp2 = round(entry * 0.97, 2)
                sl = round(entry * 1.015, 2)
                send_crypto_signal(symbol, "SHORT", str(entry), "10", str(tp1), str(tp2), str(sl), img)
                time.sleep(2)
            else:
                print(f"No signal for {symbol} currently.")
                
        except Exception as e:
            print(f"Error analyzing {symbol}: {e}")

if __name__ == "__main__":
    print("Bot started successfully...")
    analyze_and_trade()