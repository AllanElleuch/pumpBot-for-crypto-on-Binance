import math
from datetime import datetime

import FakeData

class Order:

  def __init__(self, binanceOrder, stopProfitFactor=3, stopTLossFactor=0.95 ):
    self.binanceOrder = binanceOrder
    self.coinPair = binanceOrder['symbol']
    self.buyPrice = self.get_buy_price_of_buy_order(binanceOrder)
    self.qtCoin = self.get_qt_buy_order(binanceOrder)
    self.stopProfitFactor : stopProfitFactor
    self.stopTLossFactor : stopTLossFactor
    self.stopProfit : float = float(stopProfitFactor) * self.buyPrice
    self.stopLoss : float =  float(stopTLossFactor) * self.buyPrice
    self.currentPrice = self.get_buy_price_of_buy_order(binanceOrder)
    self.timeStampUpdate = binanceOrder['transactTime']

  def timeStampToDate(self,timestamp):
    now = datetime.now().timestamp()
    if timestamp > now:
      # milliseconds, convert to seconds
      timestamp /= 1000.0
    return datetime.utcfromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

  # def __str__(self):
  #   return f'Order(coinPair={self.coinPair},change= {round((self.currentPrice/self.buyPrice*100)-100,2)}%,timeStamp= {self.timeStampToDate}buyPrice={self.buyPrice}, currentPrice={self.currentPrice}, stopProfit={self.stopProfit}, stopLoss={self.stopLoss}, binanceOrder={self.binanceOrder})'

  def __repr__(self):
    return f'Order(coinPair={self.coinPair},change= {(self.currentPrice/self.buyPrice*100)-100}%,timeStamp= {self.timeStampToDate(self.timeStampUpdate)}buyPrice={self.buyPrice}, currentPrice={self.currentPrice}, stopProfit={self.stopProfit}, stopLoss={self.stopLoss}, binanceOrder={self.binanceOrder})'

  def get_buy_price_of_buy_order(self,buyOrder):
    fills = buyOrder["fills"]
    resultOrder = next(iter(fills), None)
    priceBuy = resultOrder['price']
    return float(priceBuy)

  def get_qt_buy_order(self,buyOrder):
    qt = float(buyOrder['executedQty'])*0.9989
    return qt

  def shouldISell(self):
    if(self.currentPrice >= self.stopProfit or self.currentPrice <= self.stopLoss):
      return True
    else:
      return False


  def update(self, newPairPrice,timeStamp=datetime.now().timestamp()):
    self.currentPrice = float(newPairPrice)
    self.updateStopLoss(newPairPrice)
    self.timeStampUpdate = timeStamp

  def updateStopLoss(self, newPairPrice:float):
    if(not isinstance(newPairPrice,float)):
      newPairPrice = float(newPairPrice)


    possibleNewStopLoss = float(newPairPrice)*self.stopLoss
    if(possibleNewStopLoss > self.stopLoss):
      self.stopLoss = possibleNewStopLoss



if __name__ == "__main__":
  #fakeorder = FakeData.getFakeOrder()
  fakeorder = FakeData.getFakeOrderPrice("1.0")
  order = Order(fakeorder,1.20,0.90)
  print(order.stopLoss)
  order.updateStopLoss(1.20)
  print(order.stopLoss)
  print(order.coinPair)

  order2 = Order(FakeData.getFakeOrderPrice(4.549999999999993e-07))
  order2.update(4.149999999999993e-07)
  print(order2.shouldISell())


  order2 = Order(FakeData.getFakeOrderPrice(4.549999999999993e-07))
  order2.update(4.149999999999993e-07)
  print(order2.shouldISell())
  print(order2)
  print(str(order2))

  print(FakeData.getFakeOrderPrice("0.04",symbol="XVGBTC"))