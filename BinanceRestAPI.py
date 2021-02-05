import json
import traceback

from binance.client import Client
import logging
import math
from Logger import getLogger
import numpy as np
with open('config-binance.json') as json_data:
  api_config = json.load(json_data)
  json_data.close()

import time

class BinanceRestAPI:


  def __init__(self):
    self.data = []
    self.client = Client(api_config['api_key'], api_config['api_secret'])
    self.logger = getLogger("BinanceRestApi")
    self.exchangeInfo = self.client.get_exchange_info()

  def get_exchange_info(self):
    #self.logger.info("CACHED / exchange info")
    return self.exchangeInfo

  """
  Get balance of a crypto
  """
  def get_balance(self, symbolCrypto):
    balance = self.client.get_asset_balance(asset=symbolCrypto)
    self.logger.info("GET / balance: %s",balance)
    return balance

  def get_balance_free(self, symbolCrypto):
      balance = self.client.get_asset_balance(asset=symbolCrypto)
      balanceFree = balance['free']
      self.logger.info("GET / balance free of %s : %s",symbolCrypto,balanceFree)
      return float(balanceFree)


  def round_coin_to_step(self,pairCrypto, quantity):
    self.logger.info("Try to round coin %s %s",pairCrypto,quantity)
    try:
      coinInfo = self.getCoinInfo(pairCrypto)
      step_size = 1.0
      for f in coinInfo['filters']:
        if f['filterType'] == 'LOT_SIZE':
          step_size = float(f['stepSize'])
      # return math.floor(quantity/step_size)*step_size
      #

      numberOfZero = -math.log(step_size, 10)
      precision = int(round(numberOfZero, 0))
      formatWithStepSize = float(quantity)//step_size * step_size
      priceStopFormat ='{:.'+str(precision)+'f}'
      truncatedPrice = priceStopFormat.format(formatWithStepSize)
      qtyToSellMinusStepSize = float(truncatedPrice)
      return qtyToSellMinusStepSize
      # coinInfo =self.getCoinInfo(pairCrypto=pairCrypto)
      # targetCoinPrecision=coinInfo['baseAssetPrecision']
      # priceStopFormat ='{:.'+str(targetCoinPrecision)+'f}'
      # coin = priceStopFormat.format(quantity)
      # return float(math.roundcoin)
    except Exception as e:
      print("fail round coin ")
      print(e)
    traceback.print_exc()



  def round_price_to_step(self,pairCrypto, price, symbol_info = None ):
    self.logger.info("Try to round price %s %s",pairCrypto,price)
    try:
      if(not symbol_info):
        symbol_info = self.getCoinInfo(pairCrypto)
      step_size = 1.0
      for f in symbol_info['filters']:
        if f['filterType'] == 'PRICE_FILTER':
          step_size = float(f['minPrice'])
      #floorPart = math.floor(price/step_size)
      #result = floorPart*step_size



      numberOfZero = -math.log(step_size, 10)
      precision = int(round(numberOfZero, 0))
      qtyToSell = float(round(float(price), precision))

      #coinInfo =self.getCoinInfo(pairCrypto=pairCrypto)
      #targetCoinPrecision=coinInfo['baseAssetPrecision']
      priceStopFormat ='{:.'+str(precision)+'f}'
      formatedPrice = priceStopFormat.format(qtyToSell)

      return formatedPrice
    except Exception as e:
      print("fail round coin ")
      print(e)

  def get_open_orders(self ):
    openOrders = self.client.get_open_orders()
    self.logger.info("GET / open orders: %s",openOrders)
    return openOrders

  """ 
  use to get rounded balance of a coin to put an order on it 
  """
  def get_rounded_balance(self, pairCrypto, symbolCrypto):
    try:
      balance = self.get_balance_free(symbolCrypto=symbolCrypto)
      return self.round_coin_to_step(pairCrypto, balance)
    except Exception as e:
      print("fail get balance ")
      print(e)

  def get_balance_free_btc(self):
    return self.get_balance("BTC")['free']

  def get_buy_price_of_buy_order(self,buyOrder):
    fills = buyOrder["fills"]
    resultOrder = next(iter(fills), None)
    priceBuy = resultOrder['price']
    return float(priceBuy)

  def get_executedQty_of_buy_order(self,buyOrder):
    return float(buyOrder['executedQty'])

  """
  Get balance of all crypto in account
  """
  def get_account(self):
    return self.client.get_account()

  """
  Filter failure: MIN_NOTIONAL
  not enough money
  """
  def make_market_order_buy(self,pairCrypto,quantityInBTC):
      try:
        buyOrder =  self.client.create_order(
        symbol=pairCrypto,
        side=Client.SIDE_BUY,
        type=Client.ORDER_TYPE_MARKET,
        quoteOrderQty=quantityInBTC)
        self.logger.info("PUT / market buy order of %s $%s: %s",quantityInBTC ,pairCrypto,buyOrder)
        return buyOrder
      except Exception as e:
        self.logger.error("FAILED market buy order of %s $%s: %s : ",quantityInBTC ,pairCrypto,e)


  def make_market_order_sell(self,pairCrypto,quantityCoin):
    try:
      sellOrder = self.client.create_order(
      symbol=pairCrypto,
      side=Client.SIDE_SELL,
      type=Client.ORDER_TYPE_MARKET,
      quantity=quantityCoin)
      self.logger.info("PUT / market sell order of %s $%s: %s",quantityCoin, pairCrypto, sellOrder)
      return sellOrder
    except Exception as e:
      self.logger.error("Failed to make market order sell with %s $%s",pairCrypto,quantityCoin)
      self.logger.error(e)



  def make_market_order_sell_with_fallback(self,pairCrypto,quantityCoin):
    #listOfOrder = self.client.get_open_orders()
    #for order in listOfOrder:
    #  client.cancel_order(orderToCancel=order)
    return "NI"


  def make_market_order_sell_with_fallback(self,pairCrypto,quantityCoin):
    try:
      sellOrder = self.client.create_order(
          symbol=pairCrypto,
          side=Client.SIDE_SELL,
          type=Client.ORDER_TYPE_MARKET,
          quantity=quantityCoin)
      self.logger.info("PUT / market sell order of %s $%s: %s",quantityCoin, pairCrypto, sellOrder)
      return sellOrder
    except Exception as e:
      self.logger.error("Fail to market sell %s", pairCrypto)
      self.logger.error("Performing fall back")


  def make_order_sell_allin(self, symbolToSell, pairToSell):
    balanceCoin = self.get_balance_free(symbolToSell)
    roundedAmount = self.round_coin_to_step(pairCrypto=pairToSell,quantity=balanceCoin)
    time.sleep(0.2)
    return self.make_market_order_sell(pairCrypto=pairToSell,quantityCoin=roundedAmount)

  def make_order_buy_allin(self, pairCrypto):
    amountInBTC = self.get_balance_free_btc()
    return self.make_market_order_buy(pairCrypto,amountInBTC)

  #def make_order_take_profit_allin(self, symbolToTakeProfit,pairToTakeProfit):
  #  amountInBTC = self.get_balance(symbolToTakeProfit)
  # return self.makep(pairToTakeProfit,amountInBTC)

  def make_order_take_profit(self, pairToTakeProfit, quantityCoin, priceStop, price):
    # coinInfo =self.getCoinInfo(pairCrypto=pairToTakeProfit)
    # targetCoinPrecision=coinInfo['baseAssetPrecision']
    # priceStopFormat ='{:.'+str(targetCoinPrecision)+'f}'
    # coin = priceStopFormat.format(quantityCoin)
    roundCoin = self.round_coin_to_step(pairCrypto=pairToTakeProfit,quantity=quantityCoin)
    roundPrice = self.round_price_to_step(pairCrypto=pairToTakeProfit,price=price )

    try :
        order =   self.client.create_order(
        symbol=pairToTakeProfit,
        side=Client.SIDE_SELL,
        type=Client.ORDER_TYPE_TAKE_PROFIT_LIMIT,
        quantity=roundCoin,
        stopPrice=roundPrice,
        price=roundPrice,
        timeInForce="GTC")
        self.logger.info("PUT / market order take profit of %s $%s @%s : %s",quantityCoin, pairToTakeProfit, priceStop, priceStop)
        return order
    except Exception as e : # Failled to put order take profit ETHBTC 0.16 0.15380750 0.15380750 : APIError(code=-1013): Filter failure: PRICE_FILTER
      self.logger.error("Failled to put order take profit %s %s %s %s : %s", pairToTakeProfit, quantityCoin, priceStop, priceStop, e)

  def make_order_take_profit_from_order(self, order,multiplayer,balanceTargetCoin ):
    buyPrice = self.get_buy_price_of_buy_order(order)
    computedStop = multiplayer * buyPrice
    #targetCoinPrecision=self.client.getCoinInfo(pairCrypto=pairInBTCOfTargetCoin)['baseAssetPrecision']
   # priceStopFormat ='{:.'+str(targetCoinPrecision)+'f}'
    #priceStop = priceStopFormat.format(computedStop)


    # TAKE PROFIT
    takeProfitOrder = self.make_order_take_profit(order['symbol'],balanceTargetCoin,computedStop,computedStop)
    return takeProfitOrder

  async def  make_order_take_profit_from_order_async(self, order,multiplayer,targetCoinPrecision,balanceTargetCoin ):
    self.make_order_take_profit_from_order(order,multiplayer,targetCoinPrecision,balanceTargetCoin )

  def getCoinInfo(self,pairCrypto):
      exchangeInfo = self.exchangeInfo
      targetCoinInfo = None
      for x in exchangeInfo['symbols']:
        if(x['symbol'])== pairCrypto:
          targetCoinInfo = x
      #self.logger.info("CACHED / get coin info %s: %s",pairCrypto,targetCoinInfo)
      return targetCoinInfo
  """
  use to cancel take profit
  """
  def cancel_order(self, orderToCancel):
    try:
      self.client.cancel_order(symbol=orderToCancel['symbol'], orderId=orderToCancel['orderId'], )
      self.logger.info("PUT / cancel order n°%s - %s",orderToCancel['orderId'],orderToCancel['symbol'])
    except Exception as e:
      self.logger.error("Fail to undo order %s",orderToCancel)
      self.logger.error(e)

  def get_all_pending_orders(self):
    self.client.get_all_orders()
  def formatStopForCoin(self,pairInBTCOfTargetCoin,stop):
    targetCoinInfo = self.client.getCoinInfo(pairInBTCOfTargetCoin)
    targetCoinPrecision=targetCoinInfo['baseAssetPrecision']
    priceStopFormat ='{:.'+str(targetCoinPrecision)+'f}'
    return priceStopFormat.format(stop)



if __name__ == "__main__":
  binanceRestAPI =  BinanceRestAPI()
  binanceRestAPI.logger.error("test")
  #binanceRestAPI.make_order_take_profit("ETHBTC",0.16,0.15380750,0.15380750)
  #binanceRestAPI.make_order_take_profit("ETHBTC",50.120000000000005, 0.0062388, 0.0062388)
  #binanceRestAPI.make_order_take_profit("ETHBTC",0.10238725, 0.13541999999999998, 0.13541999999999998 )
  #binanceRestAPI.make_order_take_profit("ETHBTC",5838.0, 7.769999999999999e-05 , 7.769999999999999e-05  )
  #print(binanceRestAPI.round_coin_to_step("PNTBTC",409.64))
  # take profit ETHBTC -1.125 0.159572 0.159572 : APIError(code=-1100): Illegal characters found in parameter 'quantity'; legal range is '^([0-9]{1,20})(\.[0-
  # binanceRestAPI.make_order_take_profit("ETHBTC",5838.0, 0.159572 , 0.159572  )
  # print(binanceRestAPI.round_coin_to_step(pairCrypto="ETHBTC",quantity=float(0.5014478)))
  # print(binanceRestAPI.getCoinInfo("PNTBTC"))
  # print(binanceRestAPI.get_rounded_balance("PNTBTC","PNT"))
  # print(binanceRestAPI.round_coin_to_step("PNTBTC",1.5))
  # binanceRestAPI.make_order_take_profit("PNTBTC",1.0, 6.621e-05 , 6.621e-05 )
  #binanceRestAPI.make_order_sell_allin(pairToSell="SKYBTC",symbolToSell="SKY")
  print(binanceRestAPI.round_coin_to_step("ETHBTC",0.22927577))
  print(binanceRestAPI.round_coin_to_step("SKYBTC",0.22927577))
  print(binanceRestAPI.round_coin_to_step("PNTBTC",0.22927577))
