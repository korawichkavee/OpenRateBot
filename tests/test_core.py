from datetime import date
from decimal import Decimal
import pytest
from openratebot.database import Database
from openratebot.exchange.models import RateQuote
from openratebot.exchange.provider import invert_rate
from openratebot.services.rates import RateService
class Fake:
    name='fake'
    async def rate(self,b,q): return RateQuote(date(2026,10,6),b,q,{('USD','THB'):Decimal('33.5'),('THB','USD'):Decimal('0.029850746268656716') }[(b,q)])
    async def latest_rates(self,*a,**k): return []
    async def historical_rates(self,*a,**k): return []
    async def currencies(self): return []
def test_inverse(): assert invert_rate(Decimal('2'))==Decimal('0.5')
@pytest.mark.asyncio
async def test_conversion(tmp_path):
    s=RateService(Database(str(tmp_path/'x.db')),Fake()); result,r=await s.convert(Decimal('100'),'USD','THB'); assert result==Decimal('3350.0'); assert r.rate==Decimal('33.5')
@pytest.mark.asyncio
async def test_same(tmp_path):
    s=RateService(Database(str(tmp_path/'x.db')),Fake()); result,r=await s.convert(Decimal('100'),'THB','THB'); assert result==Decimal('100') and r.rate==Decimal('1')
def test_db(tmp_path):
    db=Database(str(tmp_path/'x.db')); q=RateQuote(date(2026,10,6),'USD','THB',Decimal('33.5')); db.save_rates([q],'fake'); assert db.get_rate('USD','THB','fake').rate==Decimal('33.5')
