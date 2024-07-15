import asyncio
import websockets
import json

msg = \
{
  "jsonrpc" : "2.0",
  "id" : 8387,
  "method" : "public/get_historical_volatility",
  "params" : {
    "currency" : "BTC"
  }
}

async def call_api(msg):
   async with websockets.connect('wss://test.deribit.com/ws/api/v2') as websocket:
       await websocket.send(msg)
       while websocket.open:
           response = await websocket.recv()
           print(response)

asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))