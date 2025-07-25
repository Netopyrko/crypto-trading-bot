import asyncio
from telegram import Bot
from telegram.error import TelegramError

class Notifier:
    def __init__(self, config):
        token       = config['telegram_token']
        chat_id     = config['telegram_chat_id']
        self.bot    = Bot(token=token)
        self.chat_id = chat_id
        self.trade_real = config['trade_real']

    def send(self, text: str):
        try:
            asyncio.run(self.bot.send_message(chat_id=self.chat_id, text=text))
        except TelegramError as e:
            print(f"‼️ Chyba při odesílání Telegram zprávy: {e}")
        except Exception as e:
            print(f"‼️ Neočekávaná chyba při odesílání zprávy: {e}")

    def notify_trade(self, order_result):
        if order_result is None or order_result.get('status') == 'paper':
            return
        side   = order_result.get('side')
        amount = order_result.get('amount')
        symbol = order_result.get('symbol')
        price  = order_result.get('price', 'n/a')
        msg = f"🔔 Obchod proveden: {side.upper()} {amount} {symbol} @ {price}"
        self.send(msg)

    def notify_error(self, error_msg: str):
        self.send(f"❗️ Chyba bota: {error_msg}")

    def notify_start(self):
        mode = "REAL" if self.trade_real else "PAPER"
        self.send(f"🤖 Trading bot právě naběhl v módu: {mode}")

    def notify_daily_summary(self, trades_count: int, pnl: float):
        """
        Pošle denní shrnutí: počet obchodů a PnL v USDC.
        """
        direction = "📈 Zisk" if pnl >= 0 else "📉 Ztráta"
        msg = f"{direction} za posledních 24 h: {pnl:.2f} USDC při {trades_count} obchodech."
        self.send(msg)
