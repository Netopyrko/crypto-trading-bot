import ccxt
import pandas as pd

class DataHandler:
    def __init__(self, config):
        # Vytvoříme instanci Binance (public API) – pro OHLCV data API klíče nepotřebuješ
        self.exchange = ccxt.binance({
            'enableRateLimit': True,   # CCXT respektuje limity burzy
        })
        self.symbol = config['symbol']

    def fetch_ohlcv(self, timeframe='1m', limit=100):
        """
        Stáhne OHLCV data pro daný symbol.
        timeframe: např. '1m', '5m', '1h'
        limit: počet svíček
        Vrací pandas DataFrame s timestamp, open, high, low, close, volume.
        """
        raw = self.exchange.fetch_ohlcv(self.symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(raw, columns=['timestamp','open','high','low','close','volume'])
        # Převedeme timestamp z ms na datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
