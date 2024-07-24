import asyncio
import websockets
import json
import pandas as pd

msg = {
    "jsonrpc": "2.0",
    "id": 8387,
    "method": "public/get_historical_volatility",
    "params": {
        "currency": "BTC"
    }
}

data = []

async def call_api(msg):
    async with websockets.connect('wss://test.deribit.com/ws/api/v2') as websocket:
        await websocket.send(msg)
        while websocket.open:
            response = await websocket.recv()
            response_json = json.loads(response)
            if 'result' in response_json:
                data.extend(response_json['result'])
                df = pd.DataFrame(data, columns=['timestamp', 'volatility'])
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # Convert timestamp to datetime
                df.to_csv('Data\historical_volatility.csv', index=False)

asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))
