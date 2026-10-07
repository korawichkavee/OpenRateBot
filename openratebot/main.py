import asyncio,logging
import discord
from discord.ext import tasks
from openratebot.config import load_settings
from openratebot.database import Database
from openratebot.exchange import create_provider
from openratebot.services.rates import RateService
from openratebot.services.alerts import AlertService
from openratebot.commands import about,admin,alerts,convert,currencies,history,rate,rates
logging.basicConfig(level=logging.INFO,format='%(asctime)s | %(levelname)s | %(name)s | %(message)s')
log=logging.getLogger('openratebot')
class Bot(discord.Client):
    def __init__(self,settings,db,service):
        super().__init__(intents=discord.Intents.none()); self.settings=settings; self.db=db; self.service=service; self.alert_service=AlertService(db,service,self); self.tree=discord.app_commands.CommandTree(self)
    async def setup_hook(self):
        if self.settings.guild_id:
            g=discord.Object(id=self.settings.guild_id); self.tree.copy_global_to(guild=g); await self.tree.sync(guild=g)
        else: await self.tree.sync()
        self.refresh.change_interval(hours=self.settings.update_interval_hours)
        self.refresh.start()
        self.alert_check.start()
    async def on_ready(self): log.info('Logged in as %s',self.user)
    @tasks.loop(hours=24)
    async def refresh(self):
        try: await self.service.refresh(self.settings.default_base_currency,list(self.settings.default_currencies)); await self.service.refresh_currencies(); log.info('Rates refreshed')
        except Exception: log.exception('Refresh failed; cached data remains available')
    @refresh.before_loop
    async def before_refresh(self): await self.wait_until_ready()
    @tasks.loop(hours=1)
    async def alert_check(self):
        await self.alert_service.check_once()
    @alert_check.before_loop
    async def before_alert_check(self): await self.wait_until_ready()
async def main():
    s=load_settings(); db=Database(s.database_path); provider=create_provider(s.rate_provider); service=RateService(db,provider); bot=Bot(s,db,service)
    convert.register(bot.tree,service,s.default_base_currency); rate.register(bot.tree,service); rates.register(bot.tree,service,s.default_base_currency,s.default_currencies); currencies.register(bot.tree,service); history.register(bot.tree,service); about.register(bot.tree,service); admin.register(bot.tree,db,s.default_base_currency); alerts.register(bot.tree,db,service)
    await bot.start(s.discord_token)
if __name__=='__main__': asyncio.run(main())
