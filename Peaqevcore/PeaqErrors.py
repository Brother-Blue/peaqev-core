class PeaqValueError(ValueError):
    def __init__(self, message: str):
        self.message = message

class PeaqKeyError(KeyError):
    def __init__(self, message: str):
        self.message = message