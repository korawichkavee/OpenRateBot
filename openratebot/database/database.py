from datetime import date,datetime,timezone
from decimal import Decimal
from pathlib import Path
import sqlite3
from openratebot.exchange.models import RateQuote,CurrencyInfo
class Database:
    def __init__(self,path): self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True); self._init()
    def _c(self):
        c=sqlite3.connect(self.path); c.row_factory=sqlite3.Row; return c
    def _init(self):
        with self._c() as c: c.executescript('''
CREATE TABLE IF NOT EXISTS rates(date TEXT NOT NULL,base_currency TEXT NOT NULL,quote_currency TEXT NOT NULL,rate TEXT NOT NULL,source TEXT NOT NULL,fetched_at TEXT NOT NULL,PRIMARY KEY(date,base_currency,quote_currency,source));
CREATE TABLE IF NOT EXISTS currencies(code TEXT PRIMARY KEY,name TEXT NOT NULL,symbol TEXT);
CREATE TABLE IF NOT EXISTS server_settings(guild_id INTEGER PRIMARY KEY,default_currency TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS alerts(id INTEGER PRIMARY KEY AUTOINCREMENT,guild_id INTEGER NOT NULL,channel_id INTEGER NOT NULL,user_id INTEGER NOT NULL,base_currency TEXT NOT NULL,quote_currency TEXT NOT NULL,threshold TEXT NOT NULL,direction TEXT NOT NULL,enabled INTEGER NOT NULL DEFAULT 1,last_triggered_date TEXT);
''')
    def save_rates(self,rates,source):
        now=datetime.now(timezone.utc).isoformat()
        with self._c() as c: c.executemany('INSERT OR REPLACE INTO rates VALUES(?,?,?,?,?,?)',[(r.date.isoformat(),r.base,r.quote,str(r.rate),source,now) for r in rates])
    def get_rate(self,base,quote,source=None):
        q='SELECT * FROM rates WHERE base_currency=? AND quote_currency=?'; p=[base,quote]
        if source: q+=' AND source=?'; p.append(source)
        q+=' ORDER BY date DESC LIMIT 1'
        with self._c() as c: row=c.execute(q,p).fetchone()
        return None if not row else RateQuote(date.fromisoformat(row['date']),row['base_currency'],row['quote_currency'],Decimal(row['rate']))
    def get_history(self,base,quote,start,end,source=None):
        q='SELECT * FROM rates WHERE base_currency=? AND quote_currency=? AND date>=? AND date<=?'; p=[base,quote,start.isoformat(),end.isoformat()]
        if source: q+=' AND source=?'; p.append(source)
        q+=' ORDER BY date'
        with self._c() as c: rows=c.execute(q,p).fetchall()
        return [RateQuote(date.fromisoformat(r['date']),r['base_currency'],r['quote_currency'],Decimal(r['rate'])) for r in rows]
    def save_currencies(self,items):
        with self._c() as c: c.executemany('INSERT OR REPLACE INTO currencies VALUES(?,?,?)',[(x.code,x.name,x.symbol) for x in items])
    def get_currencies(self):
        with self._c() as c: rows=c.execute('SELECT * FROM currencies ORDER BY code').fetchall()
        return [CurrencyInfo(r['code'],r['name'],r['symbol']) for r in rows]
    def set_server_currency(self,guild_id,currency):
        with self._c() as c: c.execute('INSERT INTO server_settings VALUES(?,?) ON CONFLICT(guild_id) DO UPDATE SET default_currency=excluded.default_currency',(guild_id,currency))
    def get_server_currency(self,guild_id,fallback):
        with self._c() as c: row=c.execute('SELECT default_currency FROM server_settings WHERE guild_id=?',(guild_id,)).fetchone()
        return row['default_currency'] if row else fallback
    def add_alert(self,guild_id,channel_id,user_id,base,quote,threshold,direction):
        with self._c() as c:
            x=c.execute('INSERT INTO alerts(guild_id,channel_id,user_id,base_currency,quote_currency,threshold,direction) VALUES(?,?,?,?,?,?,?)',(guild_id,channel_id,user_id,base,quote,str(threshold),direction)); return x.lastrowid
    def list_alerts(self,guild_id=None):
        q='SELECT * FROM alerts WHERE enabled=1'; p=[]
        if guild_id is not None: q+=' AND guild_id=?'; p=[guild_id]
        with self._c() as c: return c.execute(q+' ORDER BY id',p).fetchall()
    def mark_alert(self,alert_id,d):
        with self._c() as c: c.execute('UPDATE alerts SET last_triggered_date=? WHERE id=?',(d.isoformat(),alert_id))
