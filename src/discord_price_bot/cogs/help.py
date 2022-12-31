import discord
from discord.ext import commands

from ..utils import utils as utl
from ..environment import OWNER_NAME, OWNER_ID, VERSION, PREFIX

### @package help
# 
# Help Module

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['h', 'hilfe'])
    async def help(self, ctx, *params):
        if not params:
            try:
                owner = ctx.guild.get_member(OWNER_ID).mention
            except AttributeError:
                owner = OWNER_NAME
            emb = discord.Embed(title='Commands', 
                    color=utl.blue_light, 
                    description=f'Use `{PREFIX}help <module>` to get more information about a module :smiley:\n')
            cogs_desc = ''
            for cog in self.bot.cogs:
                # TODO make/check list
                if cog == "MessageListener" or cog == "Help":
                    continue
                cogs_desc += f'`{cog}` {self.bot.cogs[cog].__doc__}\n\n'

            emb.add_field(name='Modules', value=cogs_desc, inline=True)

            commands_desc = ''
            for command in self.bot.walk_commands():
                if not command.cog_name and not command.hidden:
                    commands_desc += f'{command.name} - {command.help}\n'

            if commands_desc:
                emb.add_field(name='Misc. Commands', value=commands_desc, inline=False)

            emb.set_footer(text=f"Bot is running Version: {VERSION}")
        elif len(params) == 1:
            for cog in self.bot.cogs:
                if cog.lower() == params[0].lower():
                    emb = discord.Embed(title=f'{cog} - Module', 
                            description=self.bot.cogs[cog].__doc__,
                            color=utl.green)
                    for command in self.bot.get_cog(cog).get_commands():
                        if not command.hidden:
                            if command.name == "price":
                                emb.add_field(name=f"{PREFIX}{command.name} <coin> <output-currency>", value=command.help, inline=False)
                            else:
                                emb.add_field(name=f"{PREFIX}{command.name}", value=command.help, inline=False)
                    break
            else:
                emb = discord.Embed(title="What's that?!",
                        description=f"I've never heard from a module called `{params[0]}` before :scream:",
                        color=utl.orange)
        elif len(params) > 1:
            emb = discord.Embed(title="That's too much.",
                    description="Please request only one module per request :sweat_smile:",
                    color=utl.orange
                )

        await utl.send_embed(ctx, emb)

async def setup(bot):
    await bot.add_cog(Help(bot))
