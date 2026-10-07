from .frankfurter import FrankfurterProvider
def create_provider(name):
    if name.strip().lower()=='frankfurter': return FrankfurterProvider()
    raise ValueError(f'Unknown exchange-rate provider: {name}')
