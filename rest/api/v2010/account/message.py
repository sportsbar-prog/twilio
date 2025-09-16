"""
Twilio Message Resource Module
Provides MessageList class for SMS/MMS compatibility (not supported in Kaphila)
"""

from twilio.base import TwilioRestException


class MessageList:
    """
    Message List Resource - Provides compatibility interface
    
    Note: SMS/MMS is not supported by Kaphila API
    """
    
    def __init__(self, api, account_sid: str):
        self._api = api
        self._solution = {'account_sid': account_sid}
        self._uri = f"/2010-04-01/Accounts/{account_sid}/Messages.json"
    
    def create(self, **kwargs):
        """
        Create message - Not supported by Kaphila
        
        Raises:
            TwilioRestException: Always (not supported)
        """
        raise TwilioRestException("SMS/MMS messaging is not supported by Kaphila API", code=20404)
    
    def list(self, **kwargs):
        """
        List messages - Not supported by Kaphila
        
        Returns:
            List: Empty list
        """
        return []
    
    def stream(self, **kwargs):
        """
        Stream messages - Not supported by Kaphila
        
        Returns:
            Iterator: Empty iterator
        """
        return iter([])
    
    def get(self, sid: str):
        """
        Get message by SID - Not supported by Kaphila
        
        Raises:
            TwilioRestException: Always (not supported)
        """
        raise TwilioRestException("SMS/MMS messaging is not supported by Kaphila API", code=20404)
    
    def __call__(self, sid: str):
        """
        Access message by SID - Not supported by Kaphila
        
        Raises:
            TwilioRestException: Always (not supported)
        """
        raise TwilioRestException("SMS/MMS messaging is not supported by Kaphila API", code=20404)
