import json


def getFakeOrder():
  stringResponseFromCreate = '{"symbol": "XVGBTC", "orderId": 78073274, "orderListId": -1, "clientOrderId": "2zSxKlDrRKSuIYLb8MuAPP", "transactTime": 1612217144995, "price": "0.00000000", "origQty": "226.00000000", "executedQty": "226.00000000", "cummulativeQuoteQty": "0.00009996", "status": "FILLED", "timeInForce": "GTC", "type": "MARKET", "side": "BUY", "fills": [{"price": "0.00000049", "qty": "226.00000000", "commission": "0.20400000", "commissionAsset": "XVG", "tradeId": 23035916}]}'
  ordertest = json.loads(stringResponseFromCreate)
  return ordertest

def getFakeOrderPrice(price,symbol="XVGBTC"):
  stringResponseFromCreate = '{"symbol": "'+symbol+'", "orderId": 78073274, "orderListId": -1, "clientOrderId": "2zSxKlDrRKSuIYLb8MuAPP", "transactTime": 1612217144995, "price": "0.00000000", "origQty": "226.00000000", "executedQty": "226.00000000", "cummulativeQuoteQty": "0.00009996", "status": "FILLED", "timeInForce": "GTC", "type": "MARKET", "side": "BUY", "fills": [{"price": "'+str(price)+'", "qty": "226.00000000", "commission": "0.20400000", "commissionAsset": "XVG", "tradeId": 23035916}]}'
  ordertest = json.loads(stringResponseFromCreate)
  return ordertest

