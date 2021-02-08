from datetime import datetime, timedelta
import json
import traceback
from decimal import Decimal

from binance.client import Client
import logging
import math

from binance.websockets import BinanceSocketManager

import FakeData
from Logger import getLogger, getLoggerFilename
import numpy as np

from Order import Order

with open('config-binance.json') as json_data:
  api_config = json.load(json_data)
  json_data.close()

import time
alreadyPumped = []
listOfShitoin = ["ETHBTC", "LTCBTC", "BNBBTC", "NEOBTC", "BCCBTC", "GASBTC", "HSRBTC", "MCOBTC", "WTCBTC", "LRCBTC", "QTUMBTC", "YOYOBTC", "OMGBTC", "ZRXBTC", "STRATBTC", "SNGLSBTC", "BQXBTC", "KNCBTC", "FUNBTC", "SNMBTC", "IOTABTC", "LINKBTC", "XVGBTC", "SALTBTC", "MDABTC", "MTLBTC", "SUBBTC", "EOSBTC", "SNTBTC", "ETCBTC", "MTHBTC", "ENGBTC", "DNTBTC", "ZECBTC", "BNTBTC", "ASTBTC", "DASHBTC", "OAXBTC", "ICNBTC", "BTGBTC", "EVXBTC", "REQBTC", "VIBBTC", "TRXBTC", "POWRBTC", "ARKBTC", "XRPBTC", "MODBTC", "ENJBTC", "STORJBTC", "VENBTC", "KMDBTC", "RCNBTC", "NULSBTC", "RDNBTC", "XMRBTC", "DLTBTC", "AMBBTC", "BATBTC", "BCPTBTC", "ARNBTC", "GVTBTC", "CDTBTC", "GXSBTC", "POEBTC", "QSPBTC", "BTSBTC", "XZCBTC", "LSKBTC", "TNTBTC", "FUELBTC", "MANABTC", "BCDBTC", "DGDBTC", "ADXBTC", "ADABTC", "PPTBTC", "CMTBTC", "XLMBTC", "CNDBTC", "LENDBTC", "WABIBTC", "TNBBTC", "WAVESBTC", "GTOBTC", "ICXBTC", "OSTBTC", "ELFBTC", "AIONBTC", "NEBLBTC", "BRDBTC", "EDOBTC", "WINGSBTC", "NAVBTC", "LUNBTC", "TRIGBTC", "APPCBTC", "VIBEBTC", "RLCBTC", "INSBTC", "PIVXBTC", "IOSTBTC", "CHATBTC", "STEEMBTC", "NANOBTC", "VIABTC", "BLZBTC", "AEBTC", "RPXBTC", "NCASHBTC", "POABTC", "ZILBTC", "ONTBTC", "STORMBTC", "XEMBTC", "WANBTC", "WPRBTC", "QLCBTC", "SYSBTC", "GRSBTC", "CLOAKBTC", "GNTBTC", "LOOMBTC", "BCNBTC", "REPBTC", "TUSDBTC", "ZENBTC", "SKYBTC", "CVCBTC", "THETABTC", "IOTXBTC", "QKCBTC", "AGIBTC", "NXSBTC", "DATABTC", "SCBTC", "NPXSBTC", "KEYBTC", "NASBTC", "MFTBTC", "DENTBTC", "ARDRBTC", "HOTBTC", "VETBTC", "DOCKBTC", "POLYBTC", "PHXBTC", "HCBTC", "GOBTC", "PAXBTC", "RVNBTC", "DCRBTC", "MITHBTC", "BCHABCBTC", "BCHSVBTC", "RENBTC", "BTTBTC", "ONGBTC", "FETBTC", "CELRBTC", "MATICBTC", "ATOMBTC", "PHBBTC", "TFUELBTC", "ONEBTC", "FTMBTC", "BTCBBTC", "ALGOBTC", "ERDBTC", "DOGEBTC", "DUSKBTC", "ANKRBTC", "WINBTC", "COSBTC", "COCOSBTC", "TOMOBTC", "PERLBTC", "CHZBTC", "BANDBTC", "BEAMBTC", "XTZBTC", "HBARBTC", "NKNBTC", "STXBTC", "KAVABTC", "ARPABTC", "CTXCBTC", "BCHBTC", "TROYBTC", "VITEBTC", "FTTBTC", "OGNBTC", "DREPBTC", "TCTBTC", "WRXBTC", "LTOBTC", "MBLBTC", "COTIBTC", "STPTBTC", "SOLBTC", "CTSIBTC", "HIVEBTC", "CHRBTC", "MDTBTC", "STMXBTC", "PNTBTC", "DGBBTC", "COMPBTC", "SXPBTC", "SNXBTC", "IRISBTC", "MKRBTC", "DAIBTC", "RUNEBTC", "FIOBTC", "AVABTC", "BALBTC", "YFIBTC", "JSTBTC", "SRMBTC", "ANTBTC", "CRVBTC", "SANDBTC", "OCEANBTC", "NMRBTC", "DOTBTC", "LUNABTC", "IDEXBTC", "RSRBTC", "PAXGBTC", "WNXMBTC", "TRBBTC", "BZRXBTC", "WBTCBTC", "SUSHIBTC", "YFIIBTC", "KSMBTC", "EGLDBTC", "DIABTC", "UMABTC", "BELBTC", "WINGBTC", "UNIBTC", "NBSBTC", "OXTBTC", "SUNBTC", "AVAXBTC", "HNTBTC", "FLMBTC", "SCRTBTC", "ORNBTC", "UTKBTC", "XVSBTC", "ALPHABTC", "VIDTBTC", "AAVEBTC", "NEARBTC", "FILBTC", "INJBTC", "AERGOBTC", "AUDIOBTC", "CTKBTC", "BOTBTC", "AKROBTC", "AXSBTC", "HARDBTC", "RENBTCBTC", "STRAXBTC", "FORBTC", "UNFIBTC", "ROSEBTC", "SKLBTC", "SUSDBTC", "GLMBTC", "GRTBTC", "JUVBTC", "PSGBTC", "1INCHBTC", "REEFBTC", "OGBTC", "ATMBTC", "ASRBTC", "CELOBTC", "RIFBTC", "BTCSTBTC", "TRUBTC", "CKBBTC", "TWTBTC", "FIROBTC", "LITBTC"]


def getStreamPartialBookDepthStreamListOfCoin(listcoins):
  list = []
  for coin in listcoins:
    list.append(coin.lower()+"@"+"depth5@100ms")
  return list


class BinanceRestAPI:
  def __init__(self,replay=False):
    self.data = []
    self.replay = replay
    self.client = Client(api_config['api_key'], api_config['api_secret'])
    self.logger = getLogger("BinanceRestApi")
    self.exchangeInfo = self.client.get_exchange_info()
    self.oldDictionary={"timestamp":datetime.now().timestamp(),"data":{}}
    self.updatedDictionary={"data":{}}
    self.sockets=[]
    if(not replay):
      self.startTickerStream()
    self.orders:list[Order]=[]
    self.alreadyPumped = []
    self.lastUpdateOrders =  datetime.now().timestamp()
    self.ticketIteration = 0
    self.logger.info("Binance rest API ready")
  def updateOrdersInTheTerminal(self, forceRendering = False):
    now = self.getTimeNow()
    if ( (now - self.lastUpdateOrders > 5 or forceRendering) and len(self.orders)>0):
      string = ""
      for order in self.orders:
        string+=(f"-{str(order)}\n")

      self.logger.info("%s Open orders : \n%s",len(self.orders),string)
      self.lastUpdateOrders = now


  def getTimeNow(self):
    return datetime.now().timestamp()

  def getOrders(self):
    return self.orders

  def deleteOrder(self,order):
    self.logger.info("untrack order %s ",order)
    self.orders.remove(order)

  def addOrders(self,obj):
    self.logger.info("track new order %s ",obj)
    order = Order(obj)
    self.orders.append(order)

  def resetData(self):
    self.oldDictionary =  {"timestamp":datetime.now().timestamp(),"data":{}}
    self.setAlreadyPumped([])

  def callBackTickerStream(self,msg,replay=False):

    self.updateOrdersInTheTerminal()
    self.prePumpDetectorHandler(msg['data'])

  def callBackReplay(self,msg,replay=False):
    self.updateOrdersInTheTerminal()
    self.prePumpDetectorHandler(msg)

  def startTickerStream(self,replay=False):
    bm = BinanceSocketManager(self.client)
    #bm.start_multiplex_socket(getStreamPartialBookDepthStreamListOfCoin(listOfShitoin), self.prePumpDetectorHandler) # 315.3 refresh par s


    conn_key = bm.start_multiplex_socket(['!bookTicker'], self.callBackTickerStream) # 315.3 refresh par s
    bm.start()
    self.sockets.append(bm)



  def handlerForOrders(self,pair, priceUpdate,timeStamp):
    for order in list(self.orders):
      if(pair == order.coinPair):
        if(self.replay and order.currentPrice != priceUpdate):
          self.updateOrdersInTheTerminal(True)
        order.update(priceUpdate,timeStamp)
        shouldISell = order.shouldISell()
        if(shouldISell):
          self.logger.info("PUT / handlerForOrders selling order %s ",order)
          self.make_market_order_sell(order.coinPair,order.qtCoin)
          self.deleteOrder(order)



  def getAlreadyPumped(self):
    global alreadyPumped
    return alreadyPumped

  def setAlreadyPumped(self,object):
    global alreadyPumped
    alreadyPumped = object

  def addAlreadyPumped(self,object):
    global alreadyPumped
    alreadyPumped.append(object)

  def prePumpDetectorHandler(self,coinUpdate:dict):
    global coinDictionary
    global firstRound
    global ultrashitcoin

    # if(self.ticketIteration % 3000==0):
    #  print("Service still on")
    self.ticketIteration+=1
    coins = set()
    #print(element)
    coinName = coinUpdate['s']
    # if(float(coinUpdate['a'])<0.00001):
    #   if coinName not in ultrashitcoin:
    #     ultrashitcoin.append(coinName)
    # if(coinName in mostUpdatedDictionary):
    #   mostUpdatedDictionary[coinName]+=1
    #   print(mostUpdatedDictionary[coinName])
    # else:f
    #   mostUpdatedDictionary[coinName]=0
    self.updatedDictionary['data'][coinName]=coinUpdate
    nowTime = datetime.now().timestamp()
    #self.logger.info(nowTime - coinUpdate['E'])
    deltaSinceLastUpdate = nowTime - self.oldDictionary['timestamp']
    if(deltaSinceLastUpdate > 60 * 60 * 3 ):
    #if(deltaSinceLastUpdate > 1 ):
      #print(nowTime - self.oldDictionary['timestamp'])
      #print("DATA IS OLD REFRESHING")
      self.oldDictionary =  {"timestamp":datetime.now().timestamp(),"data":{}}


    #if(firstRound):
    if(coinName not in self.oldDictionary['data']):
      if(coinName.endswith('BTC')):
        self.oldDictionary['data'][coinName]=coinUpdate
    else:
      try:

        # if not self.replay:
        #   f = open("logs/socket_stream.log", "a")
        #   f.write(json.dumps(coinUpdate)+"\n")
        #   f.close()
        priceCoinUpdateAsk = coinUpdate['a']
        priceCoinUpdateAskQT = coinUpdate['A']
        priceCoinUpdateBid = coinUpdate['b']
        priceCoinUpdateBidQT = coinUpdate['B']

        if('E' in coinUpdate):
          timeStamp =  int(coinUpdate['E'])/1000
        else:
          timeStamp = self.getTimeNow()

        self.handlerForOrders(coinName,priceUpdate=priceCoinUpdateAsk,timeStamp=timeStamp)

        coinFromDictionary = self.oldDictionary['data'][coinName]
        priceCoinUpdateAsk2 = coinFromDictionary['a']
        priceCoinUpdateAskQT2 = coinFromDictionary['A']
        priceCoinUpdateBid2 = coinFromDictionary['b']
        priceCoinUpdateBidQT2 = coinFromDictionary['B']

        delta = Decimal(priceCoinUpdateAsk)/Decimal(priceCoinUpdateAsk2)
        #delta2 = Decimal(priceCoinUpdateAsk)/Decimal(priceCoinUpdateBid)
        #print("[{}] {}  : {} BTC".format(datetime.now().time() ,coinName,delta))
        times = datetime.now().time() if not self.replay else time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(coinUpdate['C'])/1000))
        filteredCoin = coinName.replace("BTC","")

        # if(coinName=="MTHBTC"):
        #     print("[{}]  PUMP DETECTED {} with a detla of  {} BTC | old price {} | best ask price/qt {}/{}  | best bid price/qt  {}/{}"
        #           .format(times,filteredCoin,delta, priceCoinFromDictionary,  priceCoinUpdateAsk,priceCoinUpdateAskQT ,  priceCoinUpdateBid,priceCoinUpdateBidQT))

        if(delta>=1.05):
          getLoggerFilename("pumpDetector","pumpDetector.log").info("[{}]  PUMP DETECTED {} with a detla of  {} BTC | old price/Qt {}/{} | best ask price/qt {}/{}  | best bid price/qt  {}/{}".format(times,filteredCoin,delta, priceCoinUpdateAsk2,priceCoinUpdateAskQT2,  priceCoinUpdateAsk,priceCoinUpdateAskQT ,  priceCoinUpdateBid,priceCoinUpdateBidQT))


        if(delta >= 1.15   ):
          for order in self.getOrders():
            if order.coinPair == coinName:
              self.logger.info("[{}]  PUMP DETECTED {} with a detla of  {} BTC | old price {} | best ask price/qt {}/{}  | best bid price/qt  {}/{}".format(times,filteredCoin,delta, priceCoinUpdateAsk2,  priceCoinUpdateAsk,priceCoinUpdateAskQT ,  priceCoinUpdateBid,priceCoinUpdateBidQT))

          # getLoggerFilename("pumpDetector.log").info("[{}]  PUMP DETECTED {} with a detla of  {} BTC | old price {} | best ask price/qt {}/{}  | best bid price/qt  {}/{}"
          #                                            .format(times,filteredCoin,delta, priceCoinUpdateAsk2,  priceCoinUpdateAsk,priceCoinUpdateAskQT ,  priceCoinUpdateBid,priceCoinUpdateBidQT))

          if ( coinName not in self.getAlreadyPumped()):
            self.alreadyPumped.append(coinName)
            self.logger.info("[{}]  PUMP DETECTED {} with a detla of  {} BTC | old price {} | best ask price/qt {}/{}  | best bid price/qt  {}/{}"
                           .format(times,filteredCoin,delta, priceCoinUpdateAsk2,  priceCoinUpdateAsk,priceCoinUpdateAskQT ,  priceCoinUpdateBid,priceCoinUpdateBidQT))

            self.logger.info("START ORDER BUY %s ", coinName)
            self.addAlreadyPumped(coinName)
            if(True):
              quantityInBTC = 0.0003
              if(not self.replay):
                self.make_market_order_buy(pairCrypto=coinName,quantityInBTC=quantityInBTC,trackOrder=True)
                order = self.make_market_order_buy(pairCrypto=coinName,quantityInBTC=quantityInBTC,trackOrder=False)
                self.make_order_oco_from_order(order=order,multiplayertakeProfit=1.05,multiplayerStopLoss=0.95,multiplayerStopLossLimit=0.95,balanceTargetCoin=self.get_executedQty_of_buy_order(order))
              else:
                  self.logger.info("Replay mode:  Add order for %s %s",coinName,priceCoinUpdateAsk)
                  self.addOrders(FakeData.getFakeOrderPrice(priceCoinUpdateAsk,symbol=coinName))
      except Exception as e:
        self.logger.error("Error prePumpDetectorHandler ")
        traceback.print_tb(e)

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
      self.logger.info("fail round coin %s %s ", pairCrypto,  quantity)
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
    return float(buyOrder['executedQty'])*0.9989

  """
  Get balance of all crypto in account
  """
  def get_account(self):
    return self.client.get_account()

  """
  Filter failure: MIN_NOTIONAL
  not enough money
  """
  def make_market_order_buy(self,pairCrypto,quantityInBTC, trackOrder = False):

      try:
        buyOrder =  self.client.create_order(
        symbol=pairCrypto,
        side=Client.SIDE_BUY,
        type=Client.ORDER_TYPE_MARKET,
        quoteOrderQty=quantityInBTC)
        self.logger.info("PUT / market buy order of %s $%s: %s",quantityInBTC ,pairCrypto,buyOrder)
        if(trackOrder):
          self.logger.info("local / track new order %s ",buyOrder)
          self.addOrders(buyOrder)
        return buyOrder
      except Exception as e:
        self.logger.error("FAILED market buy order of %s $%s: %s : ",quantityInBTC ,pairCrypto,e)


  def make_market_order_sell(self,pairCrypto,quantityCoin):
    roundCoin = self.round_coin_to_step(pairCrypto=pairCrypto,quantity=quantityCoin)

    try:
      sellOrder = self.client.create_order(
      symbol=pairCrypto,
      side=Client.SIDE_SELL,
      type=Client.ORDER_TYPE_MARKET,
      quantity=roundCoin)
      self.logger.info("PUT / market sell order of %s qt %s: %s",quantityCoin, pairCrypto, sellOrder)
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


  def make_order_stop_loss(self,pairCrypto,quantityCoin ,priceStop, price):
    roundCoin = self.round_coin_to_step(pairCrypto=pairCrypto,quantity=quantityCoin)
    roundPrice = self.round_price_to_step(pairCrypto=pairCrypto,price=price )

    Order = self.client.create_order(
          symbol=pairCrypto,
          side=Client.SIDE_SELL,
          type=Client.ORDER_TYPE_STOP_LOSS_LIMIT,
          quantity=roundCoin,
          stopPrice=roundPrice,
          price=roundPrice,
          timeInForce="GTC")
    self.logger.info("PUT / market order stop loss of %s $%s @%s : %s",quantityCoin, pairCrypto, priceStop, priceStop)


  def make_order_oco(self,pairCrypto,quantityCoin ,price, priceStop, priceStopLimit):
    roundPrice = self.round_price_to_step(pairCrypto=pairCrypto,price=price )
    roundPriceStop = self.round_price_to_step(pairCrypto=pairCrypto,price=priceStop )
    roundCoin = self.round_coin_to_step(pairCrypto=pairCrypto,quantity=quantityCoin)

    try:
      order = self.client.order_oco_sell(
          symbol=pairCrypto,
          quantity=roundCoin,
          price=roundPrice,
          stopPrice= roundPriceStop,
          stopLimitPrice= roundPriceStop,
          stopLimitTimeInForce= 'GTC')
      self.logger.info("PUT / market order oco stop  loss of %s $%s @%s %s : %s",quantityCoin, pairCrypto, price,priceStop, priceStopLimit)
      return order
    except Exception as e :
      self.logger.error("PUT / FAIL market order oco stop  loss of %s $%s @%s %s : %s",quantityCoin, pairCrypto, price,priceStop,e)



  def make_order_take_profit_from_order(self, order,multiplayer,balanceTargetCoin ):
        buyPrice = self.get_buy_price_of_buy_order(order)
        computedStop = multiplayer * buyPrice
        #targetCoinPrecision=self.client.getCoinInfo(pairCrypto=pairInBTCOfTargetCoin)['baseAssetPrecision']
        # priceStopFormat ='{:.'+str(targetCoinPrecision)+'f}'
        #priceStop = priceStopFormat.format(computedStop)


        # TAKE PROFIT
        takeProfitOrder = self.make_order_take_profit(order['symbol'],balanceTargetCoin,computedStop,computedStop)
        return takeProfitOrder


  def make_order_oco_from_order(self, order,multiplayertakeProfit,multiplayerStopLoss,multiplayerStopLossLimit,balanceTargetCoin ):
    buyPrice = self.get_buy_price_of_buy_order(order)
    computedStop = multiplayertakeProfit * buyPrice
    computedStopLoss = multiplayerStopLoss * buyPrice
    computedStopLossLimit = multiplayerStopLossLimit * buyPrice
    #targetCoinPrecision=self.client.getCoinInfo(pairCrypto=pairInBTCOfTargetCoin)['baseAssetPrecision']
    # priceStopFormat ='{:.'+str(targetCoinPrecision)+'f}'
    #priceStop = priceStopFormat.format(computedStop)


    # TAKE PROFIT
    takeProfitOrder = self.make_order_oco(pairCrypto=order['symbol'],quantityCoin=balanceTargetCoin,price=computedStop,priceStop=computedStopLoss,priceStopLimit=computedStopLossLimit)
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

  def formatStopForCoin(self, pairInBTCOfTargetCoin,stop):
      targetCoinInfo = self.client.getCoinInfo(pairInBTCOfTargetCoin)
      targetCoinPrecision=targetCoinInfo['baseAssetPrecision']
      priceStopFormat ='{:.'+str(targetCoinPrecision)+'f}'
      return priceStopFormat.format(stop)

  def replayFile(self, filename):
    with open(filename, 'r') as reader:
      for line in reader.readlines():
        #print(line)
        tick = json.loads(line)
        self.callBackReplay(tick,replay=True)

if __name__ == "__main__":
  #binanceRestAPI =  BinanceRestAPI(replay=True)
  binanceRestAPI =  BinanceRestAPI()
  #binanceRestAPI.addOrders(FakeData.getFakeOrderPrice(5.549999999999993e-07))
  #binanceRestAPI.replayFile('pump_mth_evx.log')

  #binanceRestAPI.logger.error("test")
  #print(binanceRestAPI.client.ping());
  #binanceRestAPI.make_order_take_profit("ETHBTC",0.16,0.15380750,0.15380750)
  #binanceRestAPI.make_order_take_profit("ETHBTC",50.120000000000005, 0.0062388, 0.0062388)
  #binanceRestAPI.make_order_take_profit("ETHBTC",0.10238725, 0.13541999999999998, 0.13541999999999998 )
  #binanceRestAPI.make_order_take_profit("ETHBTC",5838.0, 7.769999999999999e-05 , 7.769999999999999e-05  )
  #print(binanceRestAPI.round_coin_to_step("PNTBTC",409.64))
  # take profit ETHBTC -1.125 0.159572 0.159572 : APIError(code=-1100): Illegal characters found in parameter 'quantity'; legal range is '^([0-9]{1,20})(\.[0-
  # binanceRestAPI.make_order_take_profit("ETHBTC",5838.0, 0.159572 , 0.159572  )
  # print(binanceRestAPI.round_coin_to_step(pairCrypto="ETHBTC",quantity=float(0.5014478)))
  #
  # print(binanceRestAPI.get_rounded_balance("PNTBTC","PNT"))
  # print(binanceRestAPI.round_coin_to_step("PNTBTC",1.5))
  #binanceRestAPI.make_order_take_profit("PNTBTC",1.0, 6.621e-05 , 6.621e-05 )
  #binanceRestAPI.make_order_sell_allin(pairToSell="SKYBTC",symbolToSell="SKY")
  #print(binanceRestAPI.round_coin_to_step("ETHBTC",0.22927577))
  #print(binanceRestAPI.round_coin_to_step("SKYBTC",0.22927577))
  #print(binanceRestAPI.round_coin_to_step("PNTBTC",0.22927577))
  #binanceRestAPI.make_order_stop_loss("XVGBTC",260,0.00000040,0.00000040)
  #13057.0 2.032e-05 2.032e-05 : APIError(code=-1013): Filter failure: PERCENT_PRICE
  #print(binanceRestAPI.getCoinInfo("VIBBTC"))
  #binanceRestAPI.make_order_take_profit("VIBBTC",13057.0, 2.032e-05 ,2.032e-05  )
  # data = binanceRestAPI.get_exchange_info()
  # list = []
  # for element in data['symbols']:
  #   if(element['symbol'].endswith("BTC")):
  #     list.append(element['symbol'])
  #list = json.dumps(list)
  #print("fini")
  #print(len(list))
  # binanceRestAPI.client.order_oco_sell(
  #     symbol="SKYBTC",
  #     quantity="10",
  #     price="0.00002696",
  #     stopPrice= "0.00002395",
  #     stopLimitPrice= "0.00002395",
  #     stopLimitTimeInForce= 'GTC')