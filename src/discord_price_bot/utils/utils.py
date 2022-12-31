import re
from typing import Union
import discord
from discord.errors import Forbidden

### @package utils
#
# The color presets, send_message() and make_embed() functions are
# included in the [discord-bot template by
# nonchris](https://github.com/nonchris/discord-bot)


blue_light = discord.Color.from_rgb(20, 255, 255)  # default color
green = discord.Color.from_rgb(142, 250, 60)   # success green
yellow = discord.Color.from_rgb(245, 218, 17)  # warning like 'hey, that's not cool'
orange = discord.Color.from_rgb(245, 139, 17)  # warning - rather critical like 'no more votes left'
red = discord.Color.from_rgb(255, 28, 25)      # error red

### @package utils
#
# Utilities and helper functions
#

async def send_embed(ctx, embed):
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile:", embed=embed)

def make_embed(title="", color=blue_light, name="‌", value="‌", footer=None) -> discord.Embed:
    emb = discord.Embed(title=title, color=color)
    emb.add_field(name=name, value=value)
    if footer:
        emb.set_footer(text=footer)
    return emb

def extract_id_from_string(content: str) -> Union[int, None]:
    match = re.match(r'(\D+|^)(\d{18})(\D+|$)', content)
    return int(match.group(2)) if match else None

def get_member_name(member: discord.Member) -> str:
    return member.nick if member.nick else member.name
