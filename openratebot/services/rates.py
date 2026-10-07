from datetime import date,timedelta
from decimal import Decimal
from openratebot.exchange.provider import invert_rate
class RateService:
    def __init__(self,db,provider): self.db=db; self.provider=provider
    async def ensure_rate(self,base,quote):
        base,quote=base.upper(),quote.upper()
        if base==quote: from openratebot.exchange.models import RateQuote; return RateQuote(date.today(),base,quote,Decimal(1))
        cached=self.db.get_rate(base,quote,self.provider.name)
        if cached: return cached
        r=await self.provider.rate(base,quote); self.db.save_rates([r],self.provider.name); return r
    async def convert(self,amount,base,quote):
        base,quote=base.upper(),quote.upper()
        if base==quote: return amount,await self.ensure_rate(base,quote)
        try:
            r=await self.ensure_rate(base,quote); return amount*r.rate,r
        except Exception:
            inv=await self.ensure_rate(quote,base); rate=invert_rate(inv.rate)
            from openratebot.exchange.models import RateQuote
            r=RateQuote(inv.date,base,quote,rate); return amount*rate,r
    async def refresh(self,base,quotes):
        rows=await self.provider.latest_rates(base.upper(),[q.upper() for q in quotes if q.upper()!=base.upper()]); self.db.save_rates(rows,self.provider.name); return rows
    async def rates_for(self,base,quotes):
        result=[]
        for quote in quotes:
            if quote.upper()==base.upper(): continue
            cached=self.db.get_rate(base.upper(),quote.upper(),self.provider.name)
            if cached: result.append(cached)
        missing=[q for q in quotes if q.upper()!=base.upper() and not self.db.get_rate(base.upper(),q.upper(),self.provider.name)]
        if missing:
            result.extend(await self.refresh(base,missing))
        return sorted(result,key=lambda x:x.quote)
    async def refresh_currencies(self):
        self.db.save_currencies(await self.provider.currencies())
    async def history(self,base,quote,days):
        end=date.today(); start=end-timedelta(days=days-1)
        rows=self.db.get_history(base.upper(),quote.upper(),start,end,self.provider.name)
        if rows: return rows
        rows=await self.provider.historical_rates(base.upper(),quote.upper(),start,end); self.db.save_rates(rows,self.provider.name); return rows
