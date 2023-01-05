import time
import pandas as pd
from binance.client import Client
from binance.enums import *

import ta


api_key = "*************** your binance api key ***************"
api_secret = "*************** your binance api secret ***************"

client = Client(api_key, api_secret)

# Set the symbol and time frame
symbol = "BTCUSDT"
pair_1 = "BTC"
pair_2 = "USDT"
sell_level = 16
time_frame = "1m"


iteration = 1
total_profit_loss = 0

# Set the RSI upper and lower bounds
RSI_UPPER_BOUND = 70
RSI_LOWER_BOUND = 35

def calculate_profit_loss(initial_value, final_value):
    return final_value - initial_value


while True:
    try:
        # Get the klines
        klines = client.futures_klines(symbol=symbol, interval=time_frame)

        # Get the close prices for the last 14 candlesticks
        close_prices = [candlestick[4] for candlestick in klines[-14:]]

        # Convert the close prices to floats
        close_prices = [float(price) for price in close_prices]

        # Calculate the differences between the current and previous close prices
        differences = [close_prices[i] - close_prices[i-1]
                       for i in range(1, len(close_prices))]

        # Calculate the gains and losses
        gains = [d for d in differences if d > 0]
        losses = [-d for d in differences if d < 0]

        # Calculate the average gain and loss
        avg_gain = sum(gains) / len(gains) if len(gains) > 0 else 0
        avg_loss = sum(losses) / len(losses) if len(losses) > 0 else 0

        # Calculate the relative strength
        rs = avg_gain / avg_loss if avg_loss > 0 else 0

        # Calculate the RSI
        rsi = 100 - (100 / (1 + rs))


        # Print the RSI
        print('#############################################')
        print(f"Iteration: {iteration}")
        print("Trading with", symbol)
        if (rsi > RSI_UPPER_BOUND):
            print(f"\033[31mRSI ({time_frame}): {rsi:.2f}\033[0m")
        elif (rsi < RSI_LOWER_BOUND):
            print(f"\033[32mRSI ({time_frame}): {rsi:.2f}\033[0m")
        else:
            print(f"\033[34mRSI ({time_frame}): {rsi:.2f}\033[0m")

        # RISK STRATEGY
        percent_risk = 90
        starting_balance = 59.00
        percentage = starting_balance * percent_risk / 100
        risk_slippage = 2
        level_to_not_buy = starting_balance * (100 - percent_risk + 2) / 100

        # Get the initial balances
        print('********** BALANCES **********')
        info = client.get_symbol_info(symbol)
        minQty = float(info['filters'][1]['minQty'])
        stepSize = float(info['filters'][1]['stepSize'])
        print("STEP SIZE", stepSize)
        print("MIN BUY", minQty)
        # print('info', info)
        balanceF = float(client.get_asset_balance(asset=pair_2)[
            'free'])
        balance = float(balanceF)
        print(f"Balance: {balance}")
        price = float(client.futures_ticker(
            symbol=symbol)['lastPrice'])
        print(f"Price: {price}")
        amount = round(percentage / price, 8)
        # step the amount to buy
        if (int(amount) == 0):
            amountStep = round(amount, 3)
        else:
            amountStep = int(amount)
        amountA = round(balance / price, 8)
        print(f"Amount available: {amountA}")
        print(f"Amount to risk: {amount}")
        print(f"Amount to risk step: {amountStep}")

        # print buy and sell levels
        print('RISK AMOUNT TO TRADE =', "${:.2f}".format(percentage))
        print('BAL LEVEL TO NOT BUY =', "${:.2f}".format(level_to_not_buy))

        # Get the initial balances
        initial_balance_asset_1 = float(client.get_asset_balance(asset=pair_1)[
            'free'])
        initial_balance_asset_1_int = int(initial_balance_asset_1)
        print('initial_balance_asset_1 =', initial_balance_asset_1)
        initial_balance_asset_2 = float(client.get_asset_balance(asset=pair_2)[
            'free'])
        initial_balance_asset_2_int = int(initial_balance_asset_2)
        print('initial_balance_asset_2 =', initial_balance_asset_2)
        last_priceFloat = float(client.futures_ticker(
            symbol=symbol)['lastPrice'])
        last_price_int = int(last_priceFloat)
        print('last_price =', last_priceFloat)
        initial_value_asset_1 = initial_balance_asset_1_int * \
            last_price_int

        initial_value_asset_2 = initial_balance_asset_2_int

        # Check if RSI is over over or under
        if rsi > RSI_UPPER_BOUND:
            # Sell the asset
            if (initial_balance_asset_2 < level_to_not_buy):
                order = client.order_market_sell(
                    symbol=symbol, quantity=initial_balance_asset_1)
                print(
                    "\033[31m****** Selling asset because RSI is over 70. ********\033[0m")
            else:
                print('Not enough to sell')
        elif rsi < RSI_LOWER_BOUND:
            # Buy the asset
            print(
                "\033[******* Buying asset because RSI is under 30. *******\033[0m")
            if (initial_balance_asset_2 < level_to_not_buy):
                print('Not enough money to buy')
            else:
                print('Buying', amountStep, 'of', symbol)
                if (amountStep > minQty):
                    print('GOOD TO BUY')
                    order = client.order_market_buy(
                        symbol=symbol, quantity=amountStep)
                else:
                    print(amountStep, 'NOT ENOUGH TO BUY')

        # Get the final balances
        pair_1_balance = float(
            client.get_asset_balance(asset=pair_1)['free'])
        pair_2_balance = float(
            client.get_asset_balance(asset=pair_2)['free'])
        last_price_int = int(last_priceFloat)
        final_balance_asset_1 = int(pair_1_balance)
        final_balance_asset_2 = int(pair_2_balance)
        final_value_asset_1 = final_balance_asset_1 * \
            last_price_int
        final_value_asset_2 = final_balance_asset_2

        # Calculate the profit/loss
        profit_loss_asset_1 = calculate_profit_loss(
            initial_value_asset_1, final_value_asset_1)
        profit_loss_asset_2 = calculate_profit_loss(
            initial_value_asset_2, final_value_asset_2)
        total_profit_loss += profit_loss_asset_1 + profit_loss_asset_2

        print(f"Total profit/loss: {total_profit_loss:.2f}")
        print('#############################################')
        iteration += 1
        time.sleep(30)
    except Exception as e:
        print(e)
        time.sleep(30)
