import pandas as pd
import asyncio
import websockets
import json
import time

start_timestamp = int(time.mktime(time.strptime('2024-07-19 00:00:00', '%Y-%m-%d %H:%M:%S')) * 1000)
end_timestamp = int(time.mktime(time.strptime('2024-07-23 23:59:59', '%Y-%m-%d %H:%M:%S')) * 1000)

msg_template = {
    "jsonrpc": "2.0",
    "id": 1469,
    "method": "public/get_last_trades_by_currency_and_time",
    "params": {
        "currency": "BTC",
        "start_timestamp": start_timestamp,
        "end_timestamp": end_timestamp,
        "count": 1000  # Request up to 1000 trades at a time
    }
}
data = []

async def call_api(msg):
    async with websockets.connect('wss://www.deribit.com/ws/api/v2') as websocket:
        while True:
            await websocket.send(json.dumps(msg))
            response = await websocket.recv()
            response_json = json.loads(response)
            # print(response_json)  # Print the full response for inspection
            
            if 'result' in response_json:
                trades = response_json['result'].get('trades', [])
                if not trades:
                    break
                data.extend(trades)
                if response_json['result'].get('has_more'):
                    print("There are more trades available.")
                    # Set the next start_timestamp to the timestamp of the last trade received
                    msg['params']['start_timestamp'] = trades[-1]['timestamp'] + 1
                else:
                    print("No more trades available.")
                    break
            else:
                print("No result found in response.")
                break

        df = pd.DataFrame(data)
        df.to_csv('BTC_Trades.csv', index=False)
        print("Data saved to BTC_Trades.csv")

asyncio.get_event_loop().run_until_complete(call_api(msg_template))
