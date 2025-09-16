"""
Webhook Helper for Kaphila to Twilio Conversion
"""

import json
from typing import Dict, Any


class WebhookHelper:
    """Helper class for processing Kaphila webhooks and converting to Twilio format"""
    
    @staticmethod
    def process_webhook(request_data: Dict, client) -> Dict[str, str]:
        """
        Convert Kaphila JSON webhook to Twilio form data format
        
        Args:
            request_data (Dict): Raw Kaphila webhook JSON data
            client: Twilio client instance
            
        Returns:
            Dict[str, str]: Twilio-compatible form data
        """
        twilio_data = convert_kaphila_to_twilio_webhook(request_data)
        
        # Set up context for TwiML responses
        call_sid = twilio_data.get('CallSid')
        if call_sid and client:
            if not hasattr(WebhookHelper, '_contexts'):
                WebhookHelper._contexts = {}
            WebhookHelper._contexts[call_sid] = client
            
        return twilio_data
    
    @staticmethod
    def get_client_for_call(call_sid: str):
        """Get client instance for a call"""
        if hasattr(WebhookHelper, '_contexts'):
            return WebhookHelper._contexts.get(call_sid)
        return None


def convert_kaphila_to_twilio_webhook(kaphila_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Convert Kaphila JSON webhook to Twilio form format
    
    Args:
        kaphila_data (Dict): Kaphila webhook data
        
    Returns:
        Dict[str, str]: Twilio form data format
    """
    
    if not isinstance(kaphila_data, dict) or 'event' not in kaphila_data:
        # If already in Twilio format, return as-is
        return kaphila_data
    
    # Base Twilio format
    twilio_format = {
        'CallSid': kaphila_data.get('callId', ''),
        'AccountSid': kaphila_data.get('accountSid', ''),
        'From': kaphila_data.get('from', ''),
        'To': kaphila_data.get('to', ''),
        'CallStatus': _map_call_status(kaphila_data.get('status', 'in-progress')),
        'Direction': 'outbound-api',
        'ApiVersion': '2010-04-01'
    }
    
    # Handle AMD results with custom mapping
    amd_data = kaphila_data.get('amd', {})
    if amd_data:
        status = amd_data.get('status', '').upper()
        if status == 'HUMAN':
            twilio_format['AnsweredBy'] = 'human'
        elif status == 'MACHINE':
            twilio_format['AnsweredBy'] = 'machine'
        elif status in ['NOTSURE', 'NOT_SURE']:  # "not sure" -> "human"
            twilio_format['AnsweredBy'] = 'human'
        elif status == 'UNKNOWN':  # "unknown" -> "unknown"
            twilio_format['AnsweredBy'] = 'unknown'
            
        twilio_format['MachineDetectionConfidence'] = str(amd_data.get('confidence', 0.5))
    
    # Handle DTMF events
    event_type = kaphila_data.get('event', '')
    if event_type == 'dtmf.received':
        twilio_format['Digits'] = kaphila_data.get('digit', '')
    elif event_type == 'gather.complete':
        twilio_format['Digits'] = kaphila_data.get('digits', '')
    elif event_type == 'gather.timeout':
        twilio_format['Digits'] = 'TIMEOUT'
    
    # Handle call duration
    if event_type == 'call.ended':
        twilio_format['CallDuration'] = str(kaphila_data.get('duration', 0))
        twilio_format['Duration'] = str(int(kaphila_data.get('duration', 0) / 60))
    
    # Handle recording events
    if event_type == 'recording.completed':
        twilio_format['RecordingSid'] = kaphila_data.get('recordingId', '')
        twilio_format['RecordingUrl'] = kaphila_data.get('recordingUrl', '')
        twilio_format['RecordingDuration'] = str(kaphila_data.get('duration', 0))
    
    return twilio_format


def _map_call_status(kaphila_status: str) -> str:
    """Map Kaphila status to Twilio status"""
    status_map = {
        'ringing': 'ringing',
        'answered': 'in-progress',
        'completed': 'completed',
        'failed': 'failed',
        'busy': 'busy',
        'no-answer': 'no-answer'
    }
    return status_map.get(kaphila_status.lower(), 'in-progress')
