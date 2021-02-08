import asyncio
import random
import time
q = asyncio.Queue()

res = []
async def producer(num):
  while True:
    await q.put(num + random.random())
    await asyncio.sleep(random.random())
    res.append("producer added it ")
    print(res)

async def consumer(num):
  while True:
    value = await q.get()
    print('Consumed', num, value)

loop = asyncio.get_event_loop()

for i in range(6):
  loop.create_task(producer(i))

for i in range(3):
  loop.create_task(consumer(i))

loop.run_forever()

time.sleep(2)
print(res)