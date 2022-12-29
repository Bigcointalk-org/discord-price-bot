import os
import logging
import requests
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
BTC_API_URL = 'https://min-api.cryptocompare.com/data/price?fsym=btc&tsyms=USD'
ETH_API_URL = 'https://min-api.cryptocompare.com/data/price?fsym=eth&tsyms=USD'

logging.basicConfig(format='%(message)s')
log = logging.getLogger(__name__)

def get_latest_crypto_price(crypto):
    if crypto == 'btc':
        response = requests.get(BTC_API_URL)
    elif crypto == 'eth':
        response = requests.get(ETH_API_URL)
    response_json = response.json()
    return response_json['USD']
    
def get_change(original, current):
    change = current - original
    pct_change = change / original * 100
    return pct_change

class MyClient(discord.Client):
    
    async def on_ready(self):
        print(f'We are ready...')

    async def on_message(self, message):
        global btc_last_price
        global eth_last_price
        print(f'Message from {message.author}: {message.content}')

        if message.author == self.user:
            return
        
        if message.content == '!btc':
            price = get_latest_crypto_price('btc')
            pct_change = str(round(get_change(btc_last_price, price), 2))
            btc_last_price = price
            return await message.channel.send(f'Bitcoin (BTC): {price} ({pct_change})')
        elif message.content == '!eth':
            price = get_latest_crypto_price('eth')
            pct_change = str(round(get_change(eth_last_price, price), 2))
            eth_last_price = price
            return await message.channel.send(f'Ethereum (ETH): {price} ({pct_change})')


btc_last_price = float(get_latest_crypto_price('btc'))
eth_last_price = float(get_latest_crypto_price('eth'))

print(f'Latest BTC: {btc_last_price}')
print(f'Latest ETH: {eth_last_price}')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)
