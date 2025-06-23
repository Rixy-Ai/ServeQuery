from servequery.errors import ServeQueryError


class ServeQueryLLMError(ServeQueryError):
    pass


class LLMResponseParseError(ServeQueryLLMError):
    def __init__(self, message: str, response):
        self.message = message
        self.response = response

    def get_message(self):
        return f"{self.__class__.__name__}: {self.message}"


class LLMRequestError(ServeQueryLLMError):
    def __init__(self, message: str, original_error: Exception = None):
        super().__init__(message)
        self.original_error = original_error


class LLMRateLimitError(LLMRequestError):
    pass
