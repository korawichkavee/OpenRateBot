from dataclasses import dataclass
import os
from dotenv import load_dotenv
load_dotenv()

def csv(value): return tuple(x.strip().upper() for x in value.split(',') if x.strip())

@dataclass(frozen=True)
class Settings:
    discord_token: str
    guild_id: int | None
    default_base_currency: str
    default_currencies: tuple[str,...]
    rate_provider: str
    database_path: str
    update_interval_hours: float

def load_settings():
    token=os.getenv('DISCORD_TOKEN','').strip()
    if not token: raise RuntimeError('DISCORD_TOKEN is not configured. Copy .env.example to .env.')
    raw=os.getenv('DISCORD_GUILD_ID','').strip()
    return Settings(token,int(raw) if raw else None,os.getenv('DEFAULT_BASE_CURRENCY','THB').upper(),csv(os.getenv('DEFAULT_CURRENCIES','USD,EUR,GBP,JPY,CNY,SGD')),os.getenv('RATE_PROVIDER','frankfurter').lower(),os.getenv('DATABASE_PATH','data/rates.db'),float(os.getenv('UPDATE_INTERVAL_HOURS','24')))
