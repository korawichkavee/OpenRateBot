from decimal import Decimal
SYMBOLS={'USD':'$','EUR':'€','GBP':'£','JPY':'¥','CNY':'¥','KRW':'₩','THB':'฿','SGD':'S$','AUD':'A$','CAD':'C$','CHF':'CHF '}
def amount(v): return f'{v:,.2f}'
def rate(v):
    a=abs(v)
    if a>=1000:return f'{v:,.2f}'
    if a>=1:return f'{v:,.4f}'.rstrip('0').rstrip('.')
    if a>=Decimal('0.01'):return f'{v:.6f}'.rstrip('0').rstrip('.')
    return f'{v:.8f}'.rstrip('0').rstrip('.')
def money(v,c): return f'{SYMBOLS.get(c.upper(),"")}{amount(v)} {c.upper()}'
