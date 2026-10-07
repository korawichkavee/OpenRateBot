# OpenRateBot

An open-source, self-hostable Discord bot for currency conversion and exchange rates.

**THB (Thai Baht) is the default currency, not the identity of the bot.** Any currency supported by the configured provider can be used.

## Features
- `/convert` — convert an amount between currencies
- `/rate` — inspect one pair
- `/rates` — show a base currency against configured comparison currencies
- `/history` — summarize historical rates
- `/currencies` — list supported currencies
- `/about` — bot information
- `/server_config` and `/server_currency` — per-server default currency
- `/alert` and `/alerts` — threshold alerts
- SQLite caching/history
- Daily refresh and hourly alert checks
- Provider abstraction for future exchange-rate sources
- MIT licensed and self-hostable

Default provider: [Frankfurter](https://frankfurter.dev/). Frankfurter's v2 API exposes latest, historical, time-series, and currency endpoints without an API key.

> Rates are reference rates, not guaranteed bank/card/trading execution prices.

## Quick start

```bash
git clone https://github.com/korawichkavee/OpenRateBot.git
cd openratebot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env and set DISCORD_TOKEN
python -m openratebot.main
```

The Discord bot should be invited with only the permissions it needs for slash commands and sending messages; do not grant Administrator.

## Commands

```text
/convert amount:100 from_currency:USD to_currency:THB
/convert amount:1000 to_currency:USD
/rate from_currency:USD to_currency:THB
/rates base_currency:THB
/history from_currency:USD to_currency:THB days:30
/currencies
/about
/server_config currency:USD
/server_currency
/alert from_currency:USD to_currency:THB direction:above threshold:35
/alerts
```

If `from_currency` is omitted from `/convert`, the server's default currency is used.

## Architecture

```text
Discord -> Commands -> RateService -> ExchangeRateProvider
                                      |-> FrankfurterProvider
                                      |-> future providers
                         RateService -> SQLite cache/history
```

The command layer never makes provider-specific HTTP calls. Contributors can add another provider by implementing the interface in `openratebot/exchange/provider.py`.

## Development

```bash
pip install -r requirements.txt
pytest
ruff check .
```

## Deployment

See [`deploy/INSTALL.md`](deploy/INSTALL.md) for a systemd deployment on Ubuntu. The supplied service is appropriate for a small VPS.

## License

MIT. See `LICENSE`.

## Disclaimer

This project provides informational software and is not financial advice. Verify official applicable rates for accounting, tax, settlement, or trading decisions.
