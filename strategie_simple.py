import json
import logging
import math
from logging.config import fileConfig
from BinanceRestAPI import BinanceRestAPI
import sys
from datetime import datetime
from Logger import getLogger
import time
import asyncio
import threading

logger = getLogger("example")

#often end +2 s
TIMER_SLEEP_BEFORE_CASH_OUT = 20
import time


async def make_order_take_profit_from_order_async(client, buyOrderTargetCoin, mult,multloss,multlosslimit, roundedBalanceTargetCoinMultiplayer2,start_time):
  #order = client.make_order_take_profit_from_order(order=buyOrderTargetCoin,multiplayer=mult,balanceTargetCoin=roundedBalanceTargetCoinMultiplayer2)
  order = client.make_order_oco_from_order(order=buyOrderTargetCoin,multiplayertakeProfit=mult,multiplayerStopLoss=multloss,multiplayerStopLossLimit=multlosslimit,balanceTargetCoin=roundedBalanceTargetCoinMultiplayer2)

  logger.info("--- ORDER make_order_take_profit_from_order_async  %s seconds ---" % (time.time() - start_time))
  return order

def simple_strategy(client: BinanceRestAPI,symbolTargetCoin:str, quantityInBTCToSpend: float, allIn=False):
  start_time = time.time()

  if(allIn):
    quantityInBTCToSpend = client.get_balance_free_btc()
    time.sleep(0.2)



  listOfOrder=[]
  # INIT
  pairInBTCOfTargetCoin=symbolTargetCoin+"BTC"

  #BUY ORDER
  # ex {'symbol': 'XVGBTC', 'orderId': 78255256, 'orderListId': -1, 'clientOrderId': 'FdWhnKyOIcBg50X41fqPei', 'transactTime': 1612464420265, 'price': '0.00000000', 'origQty': '319.00000000', 'executedQty': '319.00000000', 'cummulativeQuoteQty': '0.00014993', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'BUY', 'fills': [{'price': '0.00000047', 'qty': '319.00000000', 'commission': '0.31900000', 'commissionAsset': 'XVG', 'tradeId': 23087608}]}

  symbol_info = client.getCoinInfo(pairCrypto=pairInBTCOfTargetCoin)

  buyOrderTargetCoin = client.make_market_order_buy(pairCrypto=pairInBTCOfTargetCoin, quantityInBTC=quantityInBTCToSpend)
  logger.info("--- ORDER BUY IN  %s seconds ---" % (time.time() - start_time))




  balanceTargetCoin = client.round_coin_to_step(pairCrypto=pairInBTCOfTargetCoin,quantity=float(buyOrderTargetCoin['executedQty'])*0.9989)
  #balanceTargetCoin = client.get_rounded_balance(pairCrypto=pairInBTCOfTargetCoin, symbolCrypto=symbolTargetCoin)
  logger.info('Earn %s $%s', balanceTargetCoin, symbolTargetCoin)




  #buyPrice = client.get_buy_price_of_buy_order(buyOrderTargetCoin)
  #targetCoinPrecision=client.getCoinInfo(pairCrypto=pairInBTCOfTargetCoin)['baseAssetPrecision']

# do operation minus commision to estimate without call
  #qtyBought = client.get_executedQty_of_buy_order(buyOrderTargetCoin)
  #computedStop = MULTIPLAYER * buyPrice
  #MULTIPLAYER = 3.0



  #priceStopFormat ='{:.'+str(targetCoinPrecision)+'f}'
  #priceStop = priceStopFormat.format(computedStop)

  # TAKE PROFIT
  takeProfit = 1.2
  stopLoss = 0.9
  stopLimit = 0.8

  roundedBalanceTargetCoinMultiplayer1 = client.round_coin_to_step(pairCrypto=pairInBTCOfTargetCoin,quantity=balanceTargetCoin)

  roundedBalanceTargetCoinMultiplayer2 = client.round_coin_to_step(pairCrypto=pairInBTCOfTargetCoin,quantity=balanceTargetCoin*0.25)

  #   takeProfitOrder = client.make_order_take_profit_from_order_async(order=buyOrderTargetCoin,multiplayer=4.0,targetCoinPrecision=targetCoinPrecision,balanceTargetCoin=roundedBalanceTargetCoinMultiplayer3)
  #   listOfOrder.append(takeProfitOrder)
  #   takeProfitOrder = client.make_order_take_profit_from_order_async(order=buyOrderTargetCoin,multiplayer=3.5,targetCoinPrecision=targetCoinPrecision,balanceTargetCoin=roundedBalanceTargetCoinMultiplayer2)
  #   listOfOrder.append(takeProfitOrder)
  #   takeProfitOrder =
  #   listOfOrder.append(takeProfitOrder)
  t1 = threading.Thread(target=asyncio.run, args=(make_order_take_profit_from_order_async(client,buyOrderTargetCoin,takeProfit,stopLoss,stopLimit,roundedBalanceTargetCoinMultiplayer1 ,start_time), ))
  # t2 = threading.Thread(target=asyncio.run, args=(make_order_take_profit_from_order_async(client,buyOrderTargetCoin,3.5,roundedBalanceTargetCoinMultiplayer2 ,start_time), ))
  # t3 = threading.Thread(target=asyncio.run, args=(make_order_take_profit_from_order_async(client,buyOrderTargetCoin,4,balanceTargetCoin-roundedBalanceTargetCoinMultiplayer1-roundedBalanceTargetCoinMultiplayer2 ,start_time), ))
  #t2 = threading.Thread(target=asyncio.run, args=(something_async(client, pairCrypto=pairInBTCOfTargetCoin,quantity=balanceTargetCoin-roundedBalanceTargetCoinMultiplayer1-roundedBalanceTargetCoinMultiplayer2,symbol_info=symbol_info), ))
  #t3 = threading.Thread(target=asyncio.run, args=(something_async(client, pairCrypto=pairInBTCOfTargetCoin,quantity=balanceTargetCoin-roundedBalanceTargetCoinMultiplayer1-roundedBalanceTargetCoinMultiplayer2,symbol_info=symbol_info), ))


  # t1 = threading.Thread(target=asyncio.run, args=(client.make_order_take_profit_from_order_async(order=buyOrderTargetCoin,multiplayer=3.0,targetCoinPrecision=targetCoinPrecision,balanceTargetCoin=roundedBalanceTargetCoinMultiplayer1)), )
  # t2 = threading.Thread(target=asyncio.run, args=(client.make_order_take_profit_from_order_async(order=buyOrderTargetCoin,multiplayer=3.5,targetCoinPrecision=targetCoinPrecision,balanceTargetCoin=roundedBalanceTargetCoinMultiplayer2)), )
  # t3 = threading.Thread(target=asyncio.run, args=(client.make_order_take_profit_from_order_async(order=buyOrderTargetCoin,multiplayer=4,targetCoinPrecision=targetCoinPrecision,balanceTargetCoin=balanceTargetCoin-roundedBalanceTargetCoinMultiplayer1-roundedBalanceTargetCoinMultiplayer2)), )

  t1.start()
  # t2.start()
  # t3.start()
  t1.join()
  # t2.join()
  # t3.join()

  logger.info("--- ORDER TAKE PROFIT IN  %s seconds ---" % (time.time() - start_time))


  #takeProfitOrder = client.make_order_take_profit(pairInBTCOfTargetCoin,balanceTargetCoin,priceStop,priceStop)



  time.sleep(TIMER_SLEEP_BEFORE_CASH_OUT-2)

  logger.info("--- OUT OF SLEEP %s seconds ---" % (time.time() - start_time))

  time.sleep(2)
  listOfOrder = client.get_open_orders()

  for order in listOfOrder:
    client.cancel_order(orderToCancel=order)

  logger.info("--- CANCEL ORDER IN  %s seconds ---" % (time.time() - start_time))

  time.sleep(2)
  # SELL ORDER
  #orderSell = client.make_market_order_sell(pairCrypto= pairInBTCOfTargetCoin , quantityCoin= qtyBought)
  orderSell = client.make_order_sell_allin(symbolToSell=symbolTargetCoin, pairToSell=pairInBTCOfTargetCoin)
  logger.info("GREAT SUCCESS")
  logger.info("--- %s seconds ---" % (time.time() - start_time))
  logger.info("---  gain %s ---", float(buyOrderTargetCoin['cummulativeQuoteQty'])-float(orderSell['cummulativeQuoteQty']))


if __name__ == "__main__":
  binanceRestAPI =  BinanceRestAPI()
  simple_strategy(client=binanceRestAPI, symbolTargetCoin="XVG",quantityInBTCToSpend="0.00015")



  #asset = sys.stdin.readline()
  #asset = str(asset).upper().replace('\n', '')
