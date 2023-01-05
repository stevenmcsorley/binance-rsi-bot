# Binance RSI Bot
A bot that uses the relative strength index (RSI) to buy and sell assets on the Binance exchange.

## Requirements
* pandas
* binance
* ta

```bash
pip install pandas binance ta
```

## Usage
1. Replace "your binance api key" and "your binance api secret" in the script with your own Binance API key and secret.
2. Set the symbol and time frame you want to use for the RSI calculation in the script.
3. Set the RSI upper and lower bounds in the script.
4. Run the script to start the bot. The bot will continuously calculate the RSI and make trades based on the upper and lower bounds.
5. Use ctrl + c to stop the bot.

## Notes
* The bot uses a risk strategy to determine the amount of the asset to buy and sell.
* The bot has a sell level parameter which determines how many RSI cycles must pass before selling the asset. This can be adjusted in the script.
* The bot will print the RSI, balances, and price for each iteration.

## Notes on Setting Parameters

* `symbol`: This is the symbol for the asset you want to trade. It should be in the form `<pair_1>/<pair_2>`, where `pair_1` is the asset you want to buy and `pair_2` is the asset you want to sell. For example, `BTC/USDT` means you are buying Bitcoin and selling US dollars.
* `pair_1` and `pair_2`: These are the individual assets that make up the `symbol`. For example, if `symbol` is `BTC/USDT`, then `pair_1` is `BTC` and `pair_2` is `USDT`.
* `sell_level`: This is the level where if the RSI is above the UPPER_BOUND and your sell level is set to be above the balance you have of `pair_1`, then the bot will sell the asset. For example, if `sell_level` is set to `1.5`, the bot will sell the asset if the RSI is above the UPPER_BOUND and you have more than 1.5 times the balance of `pair_1` that you started with.
* `time_frame`: This is the time frame for the RSI calculation. It should be one of the time frames supported by the Binance API, such as `1m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `6h`, `8h`, `12h`, `1d`, `3d`, or `1w`.
* `RSI_UPPER_BOUND` and `RSI_LOWER_BOUND`: These are the upper and lower bounds for the RSI. When the RSI is above the upper bound, the bot will sell the asset. When the RSI is below the lower bound, the bot will buy the asset.
* `percent_risk`: This is the percentage of the balance that the bot will use to buy the asset. For example, if `percent_risk` is set to `90`, the bot will use 90% of the balance to buy the asset.
* `starting_balance`: This is the initial balance of the asset you are selling. For example, if you are selling US dollars, this is the starting balance of US dollars.
* `risk_slippage`: This is the percentage of slippage that the bot allows when buying or selling the asset. For example, if `risk_slippage` is set to `2`, the bot will allow a slippage of up to 2% when buying or selling the asset.

You should adjust these parameters to fit your specific trading strategy.

**Disclaimer:** This script is for educational and informational purposes only, and should not be used as financial advice. Trading cryptocurrency carries a high level of risk, and you should always do your own research and due diligence before making any trades. The author of this script is not  a financial advisor and is not responsible for any losses incurred as a result of using this script.
