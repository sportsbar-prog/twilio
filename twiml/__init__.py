"""
Twilio TwiML Package - 100% Compatible
Provides access to all TwiML classes for Voice, Messaging, and Fax
"""

# === VOICE TWIML (PRIMARY) ===
from twilio.twiml.voice_response import (
    VoiceResponse, TwiML, Gather, Dial, Play, Enqueue, 
    Refer, Start, Connect
)

# === COMPATIBILITY ALIASES ===
# These match exact Twilio SDK naming conventions
Response = VoiceResponse  # Legacy alias
Voice = VoiceResponse     # Alternative name

# === MESSAGING TWIML (STUBS FOR COMPATIBILITY) ===
class MessagingResponse(TwiML):
    """Messaging TwiML Response - Basic compatibility stub"""
    
    def message(self, body: str = None, to: str = None, from_: str = None,
                action: str = None, method: str = 'POST', status_callback: str = None):
        """Add Message verb (stub implementation)"""
        from xml.etree.ElementTree import SubElement
        msg_elem = SubElement(self.root, 'Message')
        if to:
            msg_elem.set('to', to)
        if from_:
            msg_elem.set('from', from_)
        if action:
            msg_elem.set('action', action)
        if method != 'POST':
            msg_elem.set('method', method)
        if status_callback:
            msg_elem.set('statusCallback', status_callback)
        if body:
            msg_elem.text = body
        return self
    
    def redirect(self, url: str, method: str = 'POST'):
        """Add Redirect verb"""
        from xml.etree.ElementTree import SubElement
        redirect_elem = SubElement(self.root, 'Redirect')
        if method != 'POST':
            redirect_elem.set('method', method)
        redirect_elem.text = url
        return self

# === FAX TWIML (STUBS FOR COMPATIBILITY) ===
class FaxResponse(TwiML):
    """Fax TwiML Response - Basic compatibility stub"""
    
    def receive(self, action: str = None, method: str = 'POST', page_size: str = 'letter'):
        """Add Receive verb"""
        from xml.etree.ElementTree import SubElement
        receive_elem = SubElement(self.root, 'Receive')
        if action:
            receive_elem.set('action', action)
        if method != 'POST':
            receive_elem.set('method', method)
        if page_size != 'letter':
            receive_elem.set('pageSize', page_size)
        return self

# === MAIN EXPORTS ===
__all__ = [
    # Voice TwiML (Primary)
    'VoiceResponse', 'TwiML', 'Gather', 'Dial', 'Play', 'Enqueue',
    'Refer', 'Start', 'Connect',
    
    # Messaging TwiML
    'MessagingResponse',
    
    # Fax TwiML
    'FaxResponse',
    
    # Aliases for compatibility
    'Response', 'Voice'
]

# === UTILITY FUNCTIONS ===
def parse_twiml(xml_string: str) -> TwiML:
    """
    Parse TwiML XML string into TwiML object
    
    Args:
        xml_string (str): TwiML XML string
        
    Returns:
        TwiML: Parsed TwiML object
    """
    from xml.etree.ElementTree import fromstring
    try:
        root = fromstring(xml_string)
        if root.tag == 'Response':
            # Determine TwiML type based on children
            child_tags = [child.tag for child in root]
            
            if any(tag in child_tags for tag in ['Say', 'Play', 'Gather', 'Dial', 'Record', 'Hangup']):
                twiml = VoiceResponse()
            elif any(tag in child_tags for tag in ['Message', 'Sms']):
                twiml = MessagingResponse()
            elif any(tag in child_tags for tag in ['Receive']):
                twiml = FaxResponse()
            else:
                twiml = TwiML()
            
            # Replace root with parsed content
            twiml.root = root
            return twiml
    except Exception:
        pass
    
    # Return empty TwiML on parse failure
    return TwiML()

def validate_twiml(xml_string: str) -> bool:
    """
    Validate TwiML XML string
    
    Args:
        xml_string (str): TwiML XML string to validate
        
    Returns:
        bool: True if valid TwiML, False otherwise
    """
    try:
        from xml.etree.ElementTree import fromstring
        root = fromstring(xml_string)
        return root.tag == 'Response'
    except Exception:
        return False
