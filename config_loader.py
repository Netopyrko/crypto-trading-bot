from dotenv import load_dotenv
import os

# Načte proměnné z .env
load_dotenv()

config = {
    # Binance API
    'api_key':        os.getenv('BINANCE_API_KEY'),
    'api_secret':     os.getenv('BINANCE_API_SECRET'),
    # Telegram
    'telegram_token': os.getenv('TELEGRAM_TOKEN'),
    'telegram_chat_id': os.getenv('TELEGRAM_CHAT_ID'),
    # Obchodní nastavení
    'symbol':         os.getenv('SYMBOL'),
    'initial_capital': float(os.getenv('INITIAL_CAPITAL')),
    'trade_amount':   float(os.getenv('TRADE_AMOUNT')),
    'stop_loss_pct':  float(os.getenv('STOP_LOSS_PCT')),
    'take_profit_pct':float(os.getenv('TAKE_PROFIT_PCT')),
    # Strategie
    'short_window':   int(os.getenv('SHORT_WINDOW')),
    'long_window':    int(os.getenv('LONG_WINDOW')),
    # Reálné obchodování (True/False)
    'trade_real':     bool(int(os.getenv('TRADE_REAL'))),
}
