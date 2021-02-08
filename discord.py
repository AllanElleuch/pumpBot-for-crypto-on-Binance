from selenium import webdriver
from getCoin import getListOfCoin
import time
from BinanceRestAPI import BinanceRestAPI

from strategie_simple import simple_strategy
#playsound('cash2.wav')
listOfCoin=getListOfCoin()
binanceRestAPI =  BinanceRestAPI()

import strategie_simple

# class MyClient(discord.Client):
#     async def on_ready(self):
#         print('Logged on as', self.user)

#     async def on_message(self, message):
#         # don't respond to ourselves
#         if message.author == self.user:
#             return

#         if message.content == 'ping':
#             await message.channel.send('pong')

# client = MyClient()
# client.run('token')
def listenWebsiteForCoin():


  driver  = webdriver.Chrome("./chromedriver")
  #wall street bets crypto coin
  #driver.get('https://discord.com/channels/804540807654408202/804540807654408206')
  # Wall street Pump
  #driver.get('https://discord.com/channels/797213409280131143/806093457667784744')
  #big signal 2
  driver.get("https://discord.com/channels/366690888321073175/806912795446607922")
  #big signal 1
  #driver.get("https://discord.com/channels/366690888321073175/806912795446607922")
  #driver.get('https://discord.com/channels/366690888321073175/806912795446607922')
  #driver.get('https://discord.com/channels/805779327403819018/805779328281083915')
  #driver.get('https://discord.com/channels/805779327403819018/806221372065054720')
  # training
  #driver.get("https://discord.com/channels/806635393524301884/806635393524301888")

  username_input = driver.find_element_by_xpath("//input[@name='email']")
  username_input.send_keys("allan.elleuch@gmail.com")
  password_input = driver.find_element_by_xpath("//input[@name='password']")
  password_input.send_keys("ican'ttestme45")
  login = driver.find_element_by_xpath("//button[@type='submit']")
  login.click()

  time.sleep(5)


  role = driver.find_element_by_xpath("//div[@role='log']")


  hasBeenFound = False
  while not hasBeenFound:
  #   returnedvalue = driver.execute_script("""
  # var element = document.querySelector("div[role=log]");
  # element.children[element.children.length-2]
  # """)
    #listOfWord = driver.execute_script('var element = document.querySelector("div[role=log]"); return element.children[element.children.length-2].outerHTML ;')
    listOfWord = driver.execute_script('return document.querySelector("div[role=log]").outerHTML ;')
    listOfWord = driver.execute_script(""" 
    htmlCollection = document.querySelector("div[role=log]").children
  var arr = [].slice.call(htmlCollection);
  arr = arr.slice(Math.max(arr.length - 5, 1))
  arr = arr.map(e=> e.innerText)
  return arr.join(" ")""")

    #listOfWord = listOfWord.upper()
    #listOfWord = listOfWord.replace("$","")
    listOfWord = listOfWord.split()
    print(listOfWord)

    for word in listOfWord:
      if("$" in word):
        word = word.replace("$","")
        word = word.upper()
        if(word in listOfCoin and word != "BTC" ):
          #playsound('target.wav')
          hasBeenFound = True
          print("Coin "+word)
          #makeMove(word, 0.00032, False)# 0.540 # 0,0013
          simple_strategy(client=binanceRestAPI, symbolTargetCoin=word,quantityInBTCToSpend="0.00055",allIn=False)

          break
          #return word
listenWebsiteForCoin()
#print()

#driver  = webdriver.Chrome("./chromedriver")
#exit(1)
#
# while True:
#   time.sleep(1000)
  #     print("The coin is " +coin)
  #
  #     makeMove(coin+"BTC", 0.1, True)
  #print(returnval)
  #time.sleep(0.02)


# script = """ 
# var $$expectedId = arguments[0];
# __selenium_observers__ =  window.__selenium_observers__ || {};
# (function(){        
# var target = document.querySelector("div[role=log]");
# __selenium_observers__[$$expectedId] = {
#         observer: new MutationObserver(function(mutations) {
#             __selenium_observers__[$$expectedId].occured = true;
#             __selenium_observers__[$$expectedId].observer.disconnect();
#         }),
#         occured:false
# };
# var config = { attributes: true, childList: true, characterData: true, subtree: true };
# __selenium_observers__[$$expectedId].observer.observe(target, config);
# })()
# """ 