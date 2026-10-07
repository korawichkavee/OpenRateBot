import discord
from discord import app_commands
from openratebot.formatting import rate

def register(tree, service, default, quotes):
    @tree.command(name='rates', description='Show several rates for a base currency.')
    async def rates_cmd(interaction, base_currency: str | None = None):
        base = (base_currency or (service.db.get_server_currency(interaction.guild_id, default) if interaction.guild_id else default)).upper()
        try:
            rows = await service.rates_for(base, list(quotes))
            if not rows:
                raise ValueError('No comparison currencies configured.')
            e = discord.Embed(title=f'💱 Exchange Rates — {base}')
            e.description = chr(10).join(f'**{r.quote}**  `{rate(r.rate)}`' for r in rows)
            e.set_footer(text=f'Reference rate: {max(r.date for r in rows)}')
            await interaction.response.send_message(embed=e)
        except Exception as exc:
            await interaction.response.send_message(f'Could not retrieve rates: `{exc}`', ephemeral=True)
