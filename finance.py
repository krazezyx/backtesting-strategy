# Basic Trading Strategy (Backtesting)

from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG
import numpy as np

# TODO: Add better risk management system (maybe ATR-based SL/TP?)

class MyStrategy(Strategy):

    def init(self):
        self.price = self.data.Close
        self.fast_sma = self.I(SMA, self.price, 10)
        self.slow_sma = self.I(SMA, self.price, 20)

        self.sl_pct = 0.03  # SL = 3% of the price
        self.tp_pct = 0.06  # TP = 6% of the price

        self.entry_price = None  # Placeholder for my entry price

        print("Indicators initialized...")  # Debugging

    # My Trading Logic for each new bar
    def next(self):
        current_price = self.data.Close[-1]

        # My SMA Crossover Strategy
        if crossover(self.fast_sma, self.slow_sma):
            print("BUY SIGNAL at", current_price)
            self.buy()
            self.entry_price = current_price

        elif self.position:  # If I have an open position...
            stop_loss = self.entry_price * (1 - self.sl_pct)
            take_profit = self.entry_price * (1 + self.tp_pct)

            if self.entry_price and (current_price <= stop_loss or current_price >= take_profit):
                print(f"Closing trade at {current_price} (SL: {stop_loss}, TP: {take_profit})")
                self.position.close()

        print(f"Current price: {current_price}, Entry: {self.entry_price}")

# Running the backtest
def main():
    print("Starting backtest...")
    bt = Backtest(GOOG, MyStrategy, cash=10000, commission=0.002, exclusive_orders=True)

    stats = bt.run()

    print("Finished Backtest...Here are the results:")
    print(stats)

    bt.plot()

if __name__ == '__main__':
    main()

# Function to log trades (not used in my backtest yet, but useful for future improvements)
def log_trade(trade_type, price, message="No extra details"):
    with open("trades.log", "a") as file:
        file.write(f"{trade_type} at {price} - {message}\n")
