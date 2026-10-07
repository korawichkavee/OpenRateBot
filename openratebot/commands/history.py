from decimal import Decimal
import discord
from discord import app_commands
from openratebot.formatting import rate

def register(tree,service):
    @tree.command(name='history',description='Summarize historical exchange rates.')
    async def history(interaction,from_currency:str,to_currency:str,days:int=30):
        if not 1<=days<=365: await interaction.response.send_message('Days must be between 1 and 365.',ephemeral=True); return
        try:
            rows=await service.history(from_currency,to_currency,days)
            if not rows: raise ValueError('No observations returned.')
            vals=[x.rate for x in rows]; avg=sum(vals,Decimal(0))/len(vals); e=discord.Embed(title=f'📈 {from_currency.upper()} → {to_currency.upper()} History'); e.add_field(name='Observations',value=str(len(vals))); e.add_field(name='Lowest',value=rate(min(vals))); e.add_field(name='Highest',value=rate(max(vals))); e.add_field(name='Average',value=rate(avg)); e.set_footer(text=f'{rows[0].date} → {rows[-1].date}'); await interaction.response.send_message(embed=e)
        except Exception as exc: await interaction.response.send_message(f'Could not retrieve history: `{exc}`',ephemeral=True)
