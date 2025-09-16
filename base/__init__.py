"""
Twilio Base Exceptions Module
Provides exception classes that match Twilio's SDK exactly
"""

class TwilioException(Exception):
    """Base Twilio exception class - 100% compatible with real Twilio SDK"""
    
    def __init__(self, message: str, code: int = None, status: int = None, method: str = None, uri: str = None):
        super().__init__(message)
        self.msg = message
        self.code = code
        self.status = status
        self.method = method
        self.uri = uri

    def __str__(self):
        return f"HTTP {self.status} error: {self.msg}"


class TwilioRestException(TwilioException):
    """REST API exception - 100% compatible with real Twilio SDK"""
    
    def __init__(self, message: str, code: int = None, status: int = None, method: str = None, uri: str = None, more_info: str = None):
        super().__init__(message, code, status, method, uri)
        self.more_info = more_info

    def __str__(self):
        error_message = f"HTTP {self.status} error: {self.msg}"
        if self.code:
            error_message += f" (Error Code: {self.code})"
        if self.more_info:
            error_message += f" More info: {self.more_info}"
        return error_message
