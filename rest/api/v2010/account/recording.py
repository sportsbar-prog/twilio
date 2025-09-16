"""
Twilio Recording Resource Module
Provides RecordingList class for recording compatibility
"""

from twilio.base import TwilioRestException


class RecordingList:
    """
    Recording List Resource - Provides compatibility interface
    """
    
    def __init__(self, api, account_sid: str):
        self._api = api
        self._solution = {'account_sid': account_sid}
        self._uri = f"/2010-04-01/Accounts/{account_sid}/Recordings.json"
    
    def list(self, **kwargs):
        """
        List recordings
        
        Returns:
            List: Empty list (Kaphila may not support listing)
        """
        return []
    
    def stream(self, **kwargs):
        """
        Stream recordings
        
        Returns:
            Iterator: Empty iterator
        """
        return iter([])
    
    def get(self, sid: str):
        """
        Get recording by SID
        
        Raises:
            TwilioRestException: Not found (may not be supported)
        """
        raise TwilioRestException("Recording not found", code=20404)
    
    def __call__(self, sid: str):
        """
        Access recording by SID
        
        Raises:
            TwilioRestException: Not found (may not be supported)
        """
        raise TwilioRestException("Recording not found", code=20404)
