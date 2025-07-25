import ccxt
import time

class Executor:
    def __init__(self, config):
        self.trade_real = config['trade_real']
        self.symbol     = config['symbol']
        self.amount     = config['trade_amount']
        params = {'enableRateLimit': True}
        if self.trade_real:
            params.update({
                'apiKey':    config['api_key'],
                'secret':    config['api_secret'],
            })
        self.exchange = ccxt.binance(params)

    def execute_order(self, signal):
        side = None
        if signal == 1:
            side = 'buy'
        elif signal == -1:
            side = 'sell'
        else:
            return None

        print(f">> Plánuji {'REAL' if self.trade_real else 'PAPER'} {side.upper()} order: "
              f"{self.amount} {self.symbol}")

        # PAPER MODE
        if not self.trade_real:
            return {'status': 'paper', 'side': side, 'amount': self.amount, 'symbol': self.symbol}

        # --- LIVE MODE ---
        try:
            # 1) kontrola balancí
            balance = self.exchange.fetch_balance()
            base, quote = self.symbol.split('/')
            if side == 'buy':
                # cena market příkazu se liší, ale minimálně zkontrolujeme, že máš dost quote (USDC)
                free_quote = balance[quote]['free']
                # Zde si můžeš ještě dohledat odhad ceny, ale aspoň validuj:
                if free_quote < self.amount * 0.0001:  # nějaká malá rezerva
                    print(f"‼️ Nedostatek {quote} (máš {free_quote}), přeskočím buy.")
                    return None
            else:  # sell
                free_base = balance[base]['free']
                if free_base < self.amount:
                    print(f"‼️ Nedostatek {base} (máš {free_base}), přeskočím sell.")
                    return None

            # 2) pokus o market order
            order = self.exchange.create_market_order(self.symbol, side, self.amount)
            return order

        except ccxt.InsufficientFunds as e:
            print("‼️ Chyba: nedostatek prostředků, order zrušen:", str(e))
            return None
        except Exception as e:
            print("‼️ Neočekávaná chyba při exekuci:", str(e))
            return None
