"""
Complete Twilio Python SDK Package - 100% Compatible
Main package initialization with exact Twilio import structure
"""

# === MAIN CLIENT AND EXCEPTIONS ===
from twilio.rest import Client
from twilio.base import TwilioException, TwilioRestException

# === VERSION INFORMATION ===
__version__ = "8.2.0"  # Matching latest Twilio version format
__author__ = "Kaphila-Compatible Twilio SDK"
__email__ = "support@kaphila.com"
__url__ = "https://github.com/kaphila/twilio-python"

# === PACKAGE METADATA ===
version_info = tuple(map(int, __version__.split('.')))
version = __version__

# === MAIN EXPORTS (EXACT TWILIO COMPATIBILITY) ===
__all__ = [
    "Client",
    "TwilioException", 
    "TwilioRestException"
]

# === LAZY IMPORTS FOR PERFORMANCE ===
def __getattr__(name: str):
    """Lazy import for less commonly used modules"""
    if name == "jwt":
        from twilio import jwt
        return jwt
    elif name == "request_validator":
        from twilio import request_validator
        return request_validator
    elif name == "access_token":
        from twilio import access_token
        return access_token
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

# === COMPATIBILITY ALIASES ===
# These provide exact compatibility with official Twilio SDK patterns
Rest = Client  # Alternative name sometimes used

# === PACKAGE INFORMATION ===
def get_version() -> str:
    """Get package version string"""
    return __version__

def get_user_agent() -> str:
    """Get user agent string for HTTP requests"""
    import platform
    python_version = platform.python_version()
    system = platform.system()
    return f"twilio-python/{__version__} (Python {python_version}; {system})"
