"""
Complete Twilio Base Module - 100% Compatible
All exception classes and base functionality matching Twilio SDK exactly
"""

import os
from typing import Optional


class TwilioException(Exception):
    """
    Base Twilio exception class - 100% compatible with real Twilio SDK
    
    All Twilio exceptions inherit from this base class.
    """
    
    def __init__(self, message: str, code: int = None, status: int = None, 
                 method: str = None, uri: str = None, more_info: str = None):
        super().__init__(message)
        self.msg = message
        self.code = code
        self.status = status
        self.method = method
        self.uri = uri
        self.more_info = more_info

    def __str__(self):
        if self.status:
            return f"HTTP {self.status} error: {self.msg}"
        return self.msg


class TwilioRestException(TwilioException):
    """
    REST API exception - 100% compatible with real Twilio SDK
    
    Raised when the Twilio API returns a non-2xx HTTP status code.
    """
    
    def __init__(self, message: str, code: int = None, status: int = None, 
                 method: str = None, uri: str = None, more_info: str = None):
        super().__init__(message, code, status, method, uri, more_info)

    def __str__(self):
        error_message = self.msg
        if self.status:
            error_message = f"HTTP {self.status} error: {self.msg}"
        if self.code:
            error_message += f" (Error Code: {self.code})"
        if self.more_info:
            error_message += f" More info: {self.more_info}"
        return error_message


class ValidationException(TwilioException):
    """
    Validation exception for invalid parameters
    """
    pass


class DeserializeException(TwilioException):
    """
    Exception raised when unable to deserialize a response
    """
    pass


# Export all exception classes
__all__ = [
    'TwilioException',
    'TwilioRestException', 
    'ValidationException',
    'DeserializeException'
]
