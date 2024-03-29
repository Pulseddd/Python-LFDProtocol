class DoesNotSupportPartialContentError(Exception):
    "An error occured while connecting."
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class UnexpectedResponseError(Exception):
    "A(n) part of a response was not in the expectation range"
    def __init__(self, *args: object) -> None:
        "A(n) part of a response was not in the expectation range"
        super().__init__(*args)

class InvalidRangeError(Exception):
    "An error has occured when downloading a range chunk"
    def __init__(self, *args: object) -> None:
        "An error has occured when downloading a range chunk"
        super().__init__(*args)
