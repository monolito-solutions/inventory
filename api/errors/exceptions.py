class BaseAPIException(Exception):
    def __init__(self, message: str, code=400):
        self.error_code = code
        self.message = message
        super().__init__(message)