"""
Complete Twilio Python SDK - Package Init
100% compatible with official Twilio SDK structure and imports

This provides the exact same import experience as:
    from twilio.rest import Client
    from twilio.twiml.voice_response import VoiceResponse, Gather
    from twilio.base import TwilioException, TwilioRestException
    from twilio.webhook_helper import WebhookHelper
"""

from twilio.rest import Client
from twilio.base import TwilioException, TwilioRestException

__version__ = "1.0.0"
__author__ = "Kaphila-Compatible Twilio SDK"
__email__ = "support@kaphila.com"
__url__ = "https://github.com/kaphila/twilio-python"

# Main exports for compatibility
__all__ = [
    "Client",
    "TwilioException", 
    "TwilioRestException"
]

# Version information (matching Twilio's structure)
version_info = (1, 0, 0)
version = __version__
