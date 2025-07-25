import pandas as pd

class Strategy:
    def __init__(self, config):
        # krátké a dlouhé okno z configu
        self.short_w = config['short_window']
        self.long_w  = config['long_window']

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Přidá sloupce:
         - sma_short: klouzavý průměr z close za krátké okno
         - sma_long:  klouzavý průměr z close za dlouhé okno
         - signal:    1 při průsečíku nahoru, -1 při průsečíku dolů, 0 jinde
        Vrátí df oříznutý na platná data (dropna).
        """
        df = df.copy()
        df['sma_short'] = df['close'].rolling(self.short_w).mean()
        df['sma_long']  = df['close'].rolling(self.long_w).mean()
        df['signal']    = 0
        df.loc[df['sma_short'] > df['sma_long'],  'signal'] = 1
        df.loc[df['sma_short'] < df['sma_long'],  'signal'] = -1
        return df.dropna()
