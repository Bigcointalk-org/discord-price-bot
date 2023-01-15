from typing import Literal, Optional
import requests
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks
from ..log_setup import logger
from ..utils import utils as ut

### @package crypto
#
# Cryptocurrency bot.
#

coins_supported = []
# fiat,stable
coins_supported.append({'name': 'US Dollar', 'symbol': 'USD'})
coins_supported.append({'name': 'Tether', 'symbol': 'USDT'})
coins_supported.append({'name': 'USDC', 'symbol': 'USDC'})
# other
coins_supported.append({'name': 'Bitcoin', 'symbol': 'BTC'})
coins_supported.append({'name': 'Ethereum', 'symbol': 'ETH'})
coins_supported.append({'name': 'Ripple', 'symbol': 'XRP'})
coins_supported.append({'name': 'DogeCoin', 'symbol': 'DOGE'})
coins_supported.append({'name': 'Cardano', 'symbol': 'ADA'})
coins_supported.append({'name': 'Polygon', 'symbol': 'MATIC'})
coins_supported.append({'name': 'Dai', 'symbol': 'DAI'})
coins_supported.append({'name': 'Polkadot', 'symbol': 'DOT'})
coins_supported.append({'name': 'TRON', 'symbol': 'TRX'})
coins_supported.append({'name': 'Litecoin', 'symbol': 'LTC'})
coins_supported.append({'name': 'Shiba Inu', 'symbol': 'SHIB'})
coins_supported.append({'name': 'Solana', 'symbol': 'SOL'})
coins_supported.append({'name': 'Uniswap', 'symbol': 'UNI'})
coins_supported.append({'name': 'Avalanche', 'symbol': 'AVAX'})

class Crypto(commands.Cog):
    """Cryptocurrency related features"""

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(name='price', help="Check a price")
    async def price(self, ctx, left: str, right='usdt'):
        logger.info(f"price: left:{left} right:{right}")
        
        coin_in = search(coins_supported, left.lower())
        coin_out = search(coins_supported, right.lower())
        if coin_in and coin_out:
            price = get_latest_crypto_price(left, right)
            if price:
                await ctx.send(embed=ut.make_embed(name='Price Check', value=f'Price of '+coin_in+'/'+coin_out+' is '+str(price)))
            else:
                await ctx.send(embed=ut.make_embed(name='**Danger, Will Robinson!**', value=f'Found '+coin_in+' AND '+coin_out+' but a problem occured.'))
        else:
            await ctx.send(embed=ut.make_embed(name='**Unsupported Cryptocurrency**', value=f'__'+left+'__ OR __'+right+'__ is not yet supported.'))
            
    @commands.command(description='Convert')
    async def convert(self, ctx, left: str, right: str):
        """Research and development."""
        print(f'({right})')
        coin_in = search(coins_supported, left.lower())
        coin_out = right.split(',')
        if coin_in:
            for coin in coin_out:
                found = search(coins_supported, coin.lower())
                if found == False:
                    await ctx.send(embed=ut.make_embed(name='**Unsupported Cryptocurrency**', value=f'__'+coin+'__ is not yet supported.'))
                    return
            prices = get_latest_crypto_price_multi(left, right)
            if prices:
                prices_string = ''
                for coin, price in prices.items():
                    print(f"{coin} - {price}\n")
                    prices_string += f"{coin} - {price}\n"
                await ctx.send(embed=ut.make_embed(name='Price of '+coin_in+' ('+left.upper()+')', value=f'Converted to '+right.upper()+' \n\n'+str(prices_string)))
                return
            else:
                await ctx.send(embed=ut.make_embed(name='**Danger, Will Robinson!**', value=f'Found '+coin_in+' AND '+right+' but a problem occured.'))
        else:
            await ctx.send(embed=ut.make_embed(name='**Unsupported Cryptocurrency**', value=f'__'+left.upper()+'__ is not yet supported.'))
        
    @commands.command(description='Display PriceBot supported projects')
    async def coins(self, ctx):
        """Research and development."""
        coins_string = ''
        for coin in coins_supported:
            print(f"{coin['name']} - {coin['symbol']}\n")
            coins_string += f"{coin['name']} ({coin['symbol']})\n"
        await ctx.send(embed=ut.make_embed(name='**Supported Projects**', value=f'Currently, we support the following projects. \n\n'+str(coins_string)))
        
        
    @commands.command(description='All')
    async def all(self, ctx, left: str):
        """Converts coin to all available currencies."""
        print(f'({left})')
        coin_in = search(coins_supported, left.lower())
        coin_out = 'USD,USDT,USDC,BTC,ETH,XRP,DOGE,ADA,MATIC,DAI,DOT,TRX,LTC,SHIB,SOL,UNI,AVAX'
        right = 'USD,USDT,USDC,BTC,ETH,XRP,DOGE,ADA,MATIC,DAI,DOT,TRX,LTC,SHIB,SOL,UNI,AVAX'
        coin_out = right.split(',')
        if coin_in:
            for coin in coin_out:
                found = search(coins_supported, coin.lower())
                if found == False:
                    await ctx.send(embed=ut.make_embed(name='**Unsupported Cryptocurrency**', value=f'__'+coin+'__ is not yet supported.'))
                    return
            prices = get_latest_crypto_price_multi(left, right)
            if prices:
                prices_string = ''
                for coin, price in prices.items():
                    print(f"{coin} - {price}\n")
                    prices_string += f"{coin} - {price}\n"
                await ctx.send(embed=ut.make_embed(name='Price of '+coin_in+' ('+left.upper()+')', value=f'Converted to '+right.upper()+' \n\n'+str(prices_string)))
                return
            else:
                await ctx.send(embed=ut.make_embed(name='**Danger, Will Robinson!**', value=f'Found '+coin_in+' AND '+right+' but a problem occured.'))
        else:
            await ctx.send(embed=ut.make_embed(name='**Unsupported Cryptocurrency**', value=f'__'+left.upper()+'__ is not yet supported.'))
        

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        pass

    @tasks.loop(seconds=60)
    async def my_task(self):
        pass

def search(list, find):
    for coin in coins_supported:
        name = coin.get('name')
        symbol = coin.get('symbol').lower()
        if symbol and symbol == find:
            return name
    return False

def api_url(left: str, right: str):
    prefix = 'https://'
    api_url_out = prefix+'min-api.cryptocompare.com/data/price?fsym='+left+'&tsyms='+right
    return api_url_out

def get_latest_crypto_price(left: str, right: str):
    if left and right:
        response = requests.get(api_url(left, right))
        
    response_json = response.json()
    
    return response_json[str(right).upper()]

def get_latest_crypto_price_multi(left: str, right: str):
    if left and right:
        response = requests.get(api_url(left, right))
        
    response_json = response.json()
    print(response_json)
    return response_json
    
def get_change(original, current):
    change = current - original
    pct_change = change / original * 100
    return pct_change
    
async def setup(bot):
    await bot.add_cog(Crypto(bot))
