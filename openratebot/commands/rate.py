import discord
from discord import app_commands
from openratebot.formatting import rate

def register(tree,service):
    @tree.command(name='rate',description='Show one exchange rate.')
    async def rate_cmd(interaction,from_currency:str,to_currency:str):
        try:
            r=await service.ensure_rate(from_currency,to_currency); e=discord.Embed(title=f'💱 {r.base} → {r.quote}',description=f'**1 {r.base} = {rate(r.rate)} {r.quote}**'); e.set_footer(text=f'Reference rate: {r.date}'); await interaction.response.send_message(embed=e)
        except Exception as exc: await interaction.response.send_message(f'Could not retrieve rate: `{exc}`',ephemeral=True)
