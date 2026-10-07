from decimal import Decimal
import discord
from discord import app_commands
from openratebot.formatting import money,rate

def register(tree,service,default):
    @tree.command(name='convert',description='Convert an amount between currencies.')
    @app_commands.describe(amount='Amount',to_currency='Target currency',from_currency='Source currency; defaults to server default')
    async def convert(interaction,amount:float,to_currency:str,from_currency:str|None=None):
        try:
            a=Decimal(str(amount))
            if a<=0: raise ValueError('Amount must be greater than zero.')
            base=from_currency.upper() if from_currency else (service.db.get_server_currency(interaction.guild_id,default) if interaction.guild_id else default)
            result,r=await service.convert(a,base,to_currency)
            e=discord.Embed(title='💱 Currency Conversion'); e.add_field(name='From',value=money(a,base),inline=True); e.add_field(name='To',value=money(result,r.quote),inline=True); e.add_field(name='Rate',value=f'1 {r.base} = {rate(r.rate)} {r.quote}',inline=False); e.set_footer(text=f'Reference rate: {r.date}')
            await interaction.response.send_message(embed=e)
        except Exception as exc: await interaction.response.send_message(f'Could not convert: `{exc}`',ephemeral=True)
