from datetime import date
from decimal import Decimal
import discord

class AlertService:
    def __init__(self, db, rates, bot):
        self.db=db; self.rates=rates; self.bot=bot
    async def check_once(self):
        today=date.today()
        for row in self.db.list_alerts():
            try:
                q=await self.rates.ensure_rate(row["base_currency"],row["quote_currency"])
                threshold=Decimal(row["threshold"])
                triggered=q.rate >= threshold if row["direction"]=="above" else q.rate <= threshold
                if not triggered or row["last_triggered_date"]==today.isoformat(): continue
                channel=self.bot.get_channel(row["channel_id"])
                if channel is None:
                    try: channel=await self.bot.fetch_channel(row["channel_id"])
                    except Exception: continue
                if isinstance(channel,discord.abc.Messageable):
                    await channel.send(f"🔔 Exchange-rate alert: **1 {q.base} = {q.rate:.6g} {q.quote}** ({row['direction']} {threshold}).")
                    self.db.mark_alert(row["id"],today)
            except Exception:
                continue
