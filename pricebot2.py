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
    return response_json['USD'];

class MyClient(discord.Client):
    
    async def on_ready(self):
        print(f'We are ready...')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

        if message.author == self.user:
            return
        
        if message.content == '!btc':
            price = get_latest_crypto_price('btc')
            return await message.channel.send(f'Bitcoin (BTC): {price}')
        elif message.content == '!eth':
            price = get_latest_crypto_price('eth')
            return await message.channel.send(f'Ethereum (ETH): {price}')
            
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)
