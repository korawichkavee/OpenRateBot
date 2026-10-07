import discord
from discord import app_commands
from openratebot import __version__
def register(tree,service):
    @tree.command(name='about',description='About OpenRateBot.')
    async def about(interaction):
        e=discord.Embed(title='🌎 OpenRateBot',description='Open-source, self-hostable Discord exchange-rate bot.'); e.add_field(name='Version',value=__version__); e.add_field(name='Provider',value=service.provider.name); e.add_field(name='License',value='MIT'); e.add_field(name='Data',value='Reference rates; verify official applicable rates for financial decisions.',inline=False); await interaction.response.send_message(embed=e)
