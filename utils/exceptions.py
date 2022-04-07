class TradeError(Exception):
    pass

class CurrencyNotSupported(TradeError):
    pass


class BalanceTooLittle(TradeError):
    pass


class NotEnoughCoins(TradeError):
    pass
