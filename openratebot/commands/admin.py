import discord
from discord import app_commands

def register(tree,db,fallback):
    @tree.command(name='server_config',description='Set this server default currency.')
    @app_commands.default_permissions(manage_guild=True)
    async def server_config(interaction,currency:str):
        if interaction.guild_id is None: await interaction.response.send_message('Server only.',ephemeral=True); return
        db.set_server_currency(interaction.guild_id,currency.upper()); await interaction.response.send_message(f'✅ Default currency is now **{currency.upper()}**.')
    @tree.command(name='server_currency',description='Show this server default currency.')
    async def server_currency(interaction):
        c=db.get_server_currency(interaction.guild_id,fallback) if interaction.guild_id else fallback; await interaction.response.send_message(f'Default currency: **{c}**',ephemeral=True)
