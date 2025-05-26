class ChallengeBotException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ForbiddenException(ChallengeBotException):
    def __init__(self, message: str):
        super().__init__(message)


class ConflictException(ChallengeBotException):
    def __init__(self, message: str):
        super().__init__(message)
