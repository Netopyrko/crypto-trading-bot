import time
import traceback
from datetime import datetime, timedelta

from config_loader import config
from data_handler   import DataHandler
from strategy       import Strategy
from executor       import Executor
from notifier       import Notifier

INTERVAL_SECONDS = 300  # 5 min mezi iteracemi

def next_midnight_timestamp():
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    # půlnoc následujícího dne
    midnight = datetime(year=tomorrow.year,
                        month=tomorrow.month,
                        day=tomorrow.day,
                        hour=0, minute=0, second=0)
    return midnight.timestamp()

def run_once(notifier, capital_tracker):
    """
    Executes one cycle: fetch, signal, order, notification,
    and updates capital_tracker with the PnL from this trade.
    """
    # 1) Data
    dh = DataHandler(config)
    df = dh.fetch_ohlcv(timeframe='5m', limit=50)

    # 2) Signály
    strat = Strategy(config)
    signals = strat.generate_signals(df)
    last_signal = signals['signal'].iloc[-1]
    print(f">> Poslední signál: {last_signal}")

    # 3) Exekuce
    executor = Executor(config)
    result = executor.execute_order(last_signal)
    print(">> Výsledek exekuce:", result)

    # 4) Notifikace
    notifier.notify_trade(result)

    # 5) PnL simulace (jen paper mód)
    # cena použita pro simulaci:
    price = df['close'].iloc[-1]
    side  = 1 if last_signal == 1 else -1 if last_signal == -1 else 0
    amount = config['trade_amount'] if side != 0 else 0
    pnl = side * amount * price
    capital_tracker['current'] += pnl
    if side != 0:
        capital_tracker['trades'] += 1

if __name__ == "__main__":
    # --- inicializace ---
    notifier = Notifier(config)
    notifier.notify_start()

    print("=== Konfigurace ===")
    for k, v in config.items():
        print(f"{k:15}: {v}")
    print()

    # Stav pro denní report
    capital_tracker = {
        'initial': config['initial_capital'],
        'current': config['initial_capital'],
        'trades' : 0,
    }
    # Čas dalšího shrnutí
    next_summary_ts = next_midnight_timestamp()

    # --- hlavní smyčka ---
    while True:
        try:
            run_once(notifier, capital_tracker)
        except Exception as e:
            print("‼️ Neočekávaná chyba:", e)
            traceback.print_exc()
            notifier.notify_error(str(e))

        # Pokud je půlnoc nebo po ní, pošli shrnutí:
        now_ts = time.time()
        if now_ts >= next_summary_ts:
            pnl = capital_tracker['current'] - capital_tracker['initial']
            trades = capital_tracker['trades']
            notifier.notify_daily_summary(trades, pnl)
            # reset pro další den:
            capital_tracker['initial'] = capital_tracker['current']
            capital_tracker['trades']  = 0
            next_summary_ts = next_midnight_timestamp()

        # čekej před dalším kolem
        time.sleep(INTERVAL_SECONDS)
