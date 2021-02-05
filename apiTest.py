

import json


stringResponseFromCreate = '{"symbol": "XVGBTC", "orderId": 78073274, "orderListId": -1, "clientOrderId": "2zSxKlDrRKSuIYLb8MuAPP", "transactTime": 1612217144995, "price": "0.00000000", "origQty": "226.00000000", "executedQty": "226.00000000", "cummulativeQuoteQty": "0.00009996", "status": "FILLED", "timeInForce": "GTC", "type": "MARKET", "side": "BUY", "fills": [{"price": "0.00000049", "qty": "226.00000000", "commission": "0.20400000", "commissionAsset": "XVG", "tradeId": 23035916}]}'
orderBuy = json.loads(stringResponseFromCreate)


MULTIPLAYER = 1.5
fills = orderBuy["fills"]
resultOrder = next(iter(fills), None)
priceBuy = resultOrder['price']


quantityBuy = 0
for fill in orderBuy["fills"]:
  quantityBuy += fill['']
qtyBuy = orderBuy['executedQty']

computedStop = MULTIPLAYER * priceBuy