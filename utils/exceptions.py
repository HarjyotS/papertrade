class TradeError(Exception):
    pass

class CurrencyNotSupported(TradeError):
    pass

class BalanceTooLittle(TradeError):
    pass

class NotEnoughCoins(TradeError):
    pass


class AuthenticationError(Exception):
    pass

class AccountDoesNotExist(AuthenticationError):
    pass

class InvalidPassword(AuthenticationError):
    pass

class AccountAlreadyExists(AuthenticationError):
    pass

class InvalidToken(AuthenticationError):
    pass
