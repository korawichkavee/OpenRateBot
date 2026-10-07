from datetime import date
from decimal import Decimal
from typing import Any
import httpx
from .models import RateQuote,CurrencyInfo
BASE_URL='https://api.frankfurter.dev'
class FrankfurterError(RuntimeError): pass
class FrankfurterProvider:
    name='frankfurter'
    def __init__(self,timeout=15.0): self.timeout=timeout
    async def _get(self,path,params=None):
        async with httpx.AsyncClient(base_url=BASE_URL,timeout=self.timeout) as c:
            r=await c.get(path,params=params)
            if r.is_error:
                try: detail=r.json().get('message',r.text)
                except Exception: detail=r.text
                raise FrankfurterError(f'Frankfurter returned HTTP {r.status_code}: {detail}')
            return r.json()
    @staticmethod
    def _q(row): return RateQuote(date.fromisoformat(row['date']),row['base'].upper(),row['quote'].upper(),Decimal(str(row['rate'])))
    async def latest_rates(self,base,quotes=None):
        p={'base':base.upper()}
        if quotes: p['quotes']=','.join(q.upper() for q in quotes)
        return [self._q(x) for x in await self._get('/v2/rates',p)]
    async def rate(self,base,quote): return self._q(await self._get(f'/v2/rate/{base.upper()}/{quote.upper()}'))
    async def historical_rates(self,base,quote,start,end):
        p={'base':base.upper(),'quotes':quote.upper(),'from':start.isoformat(),'to':end.isoformat()}
        return [self._q(x) for x in await self._get('/v2/rates',p)]
    async def currencies(self):
        data=await self._get('/v2/currencies')
        return [CurrencyInfo(x['iso_code'].upper(),x['name'],x.get('symbol')) for x in data if x.get('iso_code') and x.get('name')]
