# Contributing

1. Fork the repository.
2. Create a focused feature branch.
3. Add/update tests for behavior changes.
4. Run `pytest` and `ruff check .`.
5. Update documentation for user-visible features.
6. Open a pull request explaining what changed and why.

## Provider contributions

Implement `ExchangeRateProvider` in `openratebot/exchange/provider.py`. Return the common `RateQuote` and `CurrencyInfo` models. Keep HTTP/provider-specific logic out of Discord commands.

## Design principles

- Provider-agnostic application layer.
- `Decimal` for money/rate arithmetic.
- Cache reference data and degrade gracefully when an upstream provider is unavailable.
- Never log secrets.
- Do not require Administrator permissions.
- Keep conversion logic independently testable.
