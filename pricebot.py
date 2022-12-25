import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise
            
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to Bigcointalk.org!\n\n\nDid you know...\nYou can check the price of Bitcoin by typing !btc in any channel.'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == '!btc':
        await message.channel.send('Working on it...')
    elif message.content == 'raise-exception':
        raise discord.DiscordException
        

client.run(TOKEN)