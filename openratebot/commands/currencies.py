import discord
from discord import app_commands

def register(tree, service):
    @tree.command(name='currencies', description='List supported currencies.')
    async def currencies(interaction):
        try:
            items = service.db.get_currencies()
            if not items:
                await service.refresh_currencies()
                items = service.db.get_currencies()
            e = discord.Embed(title='🌎 Supported Currencies')
            e.description = chr(10).join(f'`{x.code}` — {x.name}' for x in items[:100])
            e.set_footer(text=f'{len(items)} currencies cached')
            await interaction.response.send_message(embed=e)
        except Exception as exc:
            await interaction.response.send_message(f'Could not retrieve currencies: `{exc}`', ephemeral=True)
