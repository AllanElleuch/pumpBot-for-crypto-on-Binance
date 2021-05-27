# MoonBot

## Quick Start

Edit the file `config-binance.json` with your binance api key 

## How to use ?

Run `main.py` and enter the Coin you want to all in (i.e : 'XVG' for all in XVGBTC)

You cal also use `discord.py` to scrap a discord channel and buy a coin as soon as the coin name for a pump is released.

## Architecture

| File              | Description                                               |
|-------------------|-----------------------------------------------------------|
| BinanceRestAPI.py | Perform API call to Binance                               |
| Main.py           | Command line tool to perform an all in on a coin for pump |
