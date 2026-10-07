from decimal import Decimal
import discord
from discord import app_commands

def register(tree, db, service):
    @tree.command(name='alert', description='Create a threshold exchange-rate alert.')
    @app_commands.choices(direction=[app_commands.Choice(name='above', value='above'), app_commands.Choice(name='below', value='below')])
    async def alert(interaction, from_currency: str, to_currency: str, direction: app_commands.Choice[str], threshold: float):
        if interaction.guild_id is None:
            await interaction.response.send_message('Alerts require a server.', ephemeral=True)
            return
        try:
            await service.ensure_rate(from_currency, to_currency)
            x = db.add_alert(interaction.guild_id, interaction.channel_id or 0, interaction.user.id, from_currency.upper(), to_currency.upper(), Decimal(str(threshold)), direction.value)
            await interaction.response.send_message(f'🔔 Alert #{x} created: 1 {from_currency.upper()} {direction.value} {threshold} {to_currency.upper()}.')
        except Exception as exc:
            await interaction.response.send_message(f'Could not create alert: `{exc}`', ephemeral=True)

    @tree.command(name='alerts', description='List active exchange-rate alerts.')
    async def alerts(interaction):
        rows = db.list_alerts(interaction.guild_id)
        text = chr(10).join(f"#{r['id']} — 1 {r['base_currency']} {r['direction']} {r['threshold']} {r['quote_currency']}" for r in rows) or 'No active alerts.'
        await interaction.response.send_message(text, ephemeral=True)
