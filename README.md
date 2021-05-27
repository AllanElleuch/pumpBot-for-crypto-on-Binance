# MoonBot

This is command line python bot to perform Pump & Dump on the Binance Market. Since the last surge of crypto in January 2021 this phenomenum came back and we took an interest into diving into it.

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


## Evolution

The bot has been completely rewriten in javascript, react and electron to make a desktop application. And has been made with 5 other collaborators. A license system as also be put in place to restrict the use of the bot. You can find a video of the bot here [Youtube Link](https://www.youtube.com/watch?v=1JjoRWwkdgI). The source code is available for review on request only.

Functionallities:
- Enter into a pump manually
- Use market price analysis to enter a pump before a coin is released. 
- Order history
- Graph to visualise real-time evolution of the pair you buy
- Selling your position
