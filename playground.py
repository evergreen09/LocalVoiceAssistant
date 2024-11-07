import ccxt.async_support as ccxt
import asyncio

binance = ccxt.binance()

async def fetch_binance_ticker():
    while True:
        btcusdt_binance = await binance.fetch_ticker('BTC/USDT')
        print(btcusdt_binance['last'])

asyncio.run(fetch_binance_ticker())