import asyncio
import random
import time
q = asyncio.Queue()

res = []
async def producer(num):
    await q.put("XVG")
    print(res)
    await asyncio.sleep(2)
    await q.put("XVG")


async def consumer(num):
  end = False
  while not end:
    value = await q.get()
    print("Received " + str(value))
    value = await q.get()
    print("trigger sell " + str(value))


loop = asyncio.get_event_loop()

#for i in range(6):
loop.create_task(producer("a"))

#for i in range(3):
loop.create_task(consumer("a"))

loop.run_forever()

time.sleep(2)
print(res)