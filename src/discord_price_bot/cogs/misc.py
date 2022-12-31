from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks

from ..log_setup import logger
from ..utils import utils as ut


### @package misc
#
# Collection of misfit commands.
#
class Misc(commands.Cog):
    """Misfit commands that have no home"""

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(name='ping', help="Check if PriceBot is available")
    async def ping(self, ctx):
        logger.info(f"ping: {round(self.bot.latency * 1000)}")

        await ctx.send(
            embed=ut.make_embed(
                name='Bot is available',
                value=f'`{round(self.bot.latency * 1000)}ms`')
        )

    @app_commands.command(name="ping", description="Ping as a slash command")
    async def ping_slash(self,
                         interaction: discord.Interaction,
                         mode: Optional[Literal["silent", "loud"]]):
        logger.info(f"ping: {round(self.bot.latency * 1000)}")
        # decide whether this message shall be silent
        ephemeral = True if mode and mode == "silent" else False

        await interaction.response.send_message(
            embed=ut.make_embed(
                name='Bot is available',
                value=f'`{round(self.bot.latency * 1000)}ms`'),
            ephemeral=ephemeral
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        pass

    @tasks.loop(seconds=60)
    async def my_task(self):
        pass

async def setup(bot):
    await bot.add_cog(Misc(bot))
