"""
Twilio TwiML Voice Response Module
Provides VoiceResponse and related classes that match Twilio's TwiML exactly
"""

from xml.etree.ElementTree import Element, SubElement, tostring
from typing import Optional, List, Union


class TwiML:
    """Base TwiML class - matches Twilio's structure"""
    
    def __init__(self):
        self.root = Element('Response')
    
    def __str__(self):
        """Return XML string representation"""
        return '<?xml version="1.0" encoding="UTF-8"?>' + tostring(self.root, encoding='unicode')
    
    def to_xml(self):
        """Return XML string (alias for __str__)"""
        return str(self)


class VoiceResponse(TwiML):
    """
    TwiML Voice Response - 100% compatible with Twilio's VoiceResponse
    
    This class provides the exact same interface as Twilio's VoiceResponse
    with context-aware features for direct Kaphila API calls when possible.
    
    Usage:
        response = VoiceResponse()
        response.say("Hello World")
        gather = response.gather(num_digits=1)
        gather.say("Press 1 for sales")
        print(str(response))
    """
    
    def __init__(self):
        super().__init__()
        self._call_sid = None
        self._client = None
    
    def _set_context(self, call_sid: str, client):
        """Set context for direct API calls (internal method)"""
        self._call_sid = call_sid
        self._client = client
    
    def say(self, message: str, voice: str = None, language: str = None, loop: int = 1) -> 'VoiceResponse':
        """
        Add Say verb to speak text
        
        Args:
            message (str): Text to speak
            voice (str): Voice to use ('man', 'woman', 'alice', etc.)
            language (str): Language code ('en', 'es', 'fr', etc.)
            loop (int): Number of times to repeat
            
        Returns:
            VoiceResponse: Self for method chaining
        """
        # Context-aware: make direct API call if possible
        if self._call_sid and self._client:
            try:
                self._client.request('POST', '/voice', data={
                    'callId': self._call_sid,
                    'text': message,
                    'playTo': 'bridge'
                })
            except:
                pass  # Fallback to TwiML
        
        # Add to TwiML
        say_elem = SubElement(self.root, 'Say')
        if voice:
            say_elem.set('voice', voice)
        if language:
            say_elem.set('language', language)
        if loop != 1:
            say_elem.set('loop', str(loop))
        say_elem.text = message
        
        return self
    
    def play(self, url: str, loop: int = 1, digits: str = None) -> 'VoiceResponse':
        """
        Add Play verb to play audio
        
        Args:
            url (str): Audio file URL or filename
            loop (int): Number of times to play
            digits (str): DTMF digits to play during audio
            
        Returns:
            VoiceResponse: Self for method chaining
        """
        # Context-aware: make direct API call if possible
        if self._call_sid and self._client:
            try:
                # Extract filename from URL for Kaphila
                filename = url.split('/')[-1].split('.')[0] if '/' in url else url
                self._client.request('POST', '/play', data={
                    'callId': self._call_sid,
                    'file': filename,
                    'playTo': 'bridge'
                })
            except:
                pass  # Fallback to TwiML
        
        # Add to TwiML
        play_elem = SubElement(self.root, 'Play')
        if loop != 1:
            play_elem.set('loop', str(loop))
        if digits:
            play_elem.set('digits', digits)
        play_elem.text = url
        
        return self
    
    def gather(self, input: str = 'dtmf', action: str = None, method: str = 'POST',
               timeout: int = 5, finish_on_key: str = '#', num_digits: int = None,
               partial_result_callback: str = None, partial_result_callback_method: str = 'POST',
               language: str = 'en-US', hints: str = None, barge_in: bool = None,
               debug: bool = None, action_on_empty_result: bool = None,
               speech_timeout: str = None, enhanced: bool = None,
               speech_model: str = None, profanity_filter: bool = None) -> 'Gather':
        """
        Add Gather verb to collect user input
        
        Args:
            input (str): Input type ('dtmf', 'speech', 'dtmf speech')
            action (str): URL to send results to
            method (str): HTTP method ('GET', 'POST')
            timeout (int): Timeout in seconds
            finish_on_key (str): Key that ends input
            num_digits (int): Exact number of digits to collect
            partial_result_callback (str): URL for partial results
            partial_result_callback_method (str): Method for partial results
            language (str): Language for speech recognition
            hints (str): Speech recognition hints
            barge_in (bool): Allow barge-in during playback
            debug (bool): Enable debug mode
            action_on_empty_result (bool): Send action on empty result
            speech_timeout (str): Speech timeout setting
            enhanced (bool): Use enhanced speech recognition
            speech_model (str): Speech model to use
            profanity_filter (bool): Filter profanity
            
        Returns:
            Gather: Gather object for nesting verbs
        """
        gather_elem = SubElement(self.root, 'Gather')
        
        # Set attributes (only if different from defaults)
        if input != 'dtmf':
            gather_elem.set('input', input)
        if action:
            gather_elem.set('action', action)
        if method != 'POST':
            gather_elem.set('method', method)
        if timeout != 5:
            gather_elem.set('timeout', str(timeout))
        if finish_on_key != '#':
            gather_elem.set('finishOnKey', finish_on_key)
        if num_digits:
            gather_elem.set('numDigits', str(num_digits))
        if partial_result_callback:
            gather_elem.set('partialResultCallback', partial_result_callback)
        if partial_result_callback_method != 'POST':
            gather_elem.set('partialResultCallbackMethod', partial_result_callback_method)
        if language != 'en-US':
            gather_elem.set('language', language)
        if hints:
            gather_elem.set('hints', hints)
        if barge_in is not None:
            gather_elem.set('bargeIn', 'true' if barge_in else 'false')
        if debug is not None:
            gather_elem.set('debug', 'true' if debug else 'false')
        if action_on_empty_result is not None:
            gather_elem.set('actionOnEmptyResult', 'true' if action_on_empty_result else 'false')
        if speech_timeout:
            gather_elem.set('speechTimeout', speech_timeout)
        if enhanced is not None:
            gather_elem.set('enhanced', 'true' if enhanced else 'false')
        if speech_model:
            gather_elem.set('speechModel', speech_model)
        if profanity_filter is not None:
            gather_elem.set('profanityFilter', 'true' if profanity_filter else 'false')
        
        return Gather(gather_elem, self._call_sid, self._client)
    
    def record(self, action: str = None, method: str = 'POST', timeout: int = 5,
               finish_on_key: str = '1234567890*#', max_length: int = 3600,
               play_beep: bool = True, trim: str = 'trim-silence',
               recording_status_callback: str = None,
               recording_status_callback_method: str = 'POST',
               recording_status_callback_event: List[str] = None,
               transcribe: bool = False, transcribe_callback: str = None) -> 'VoiceResponse':
        """
        Add Record verb to record audio
        
        Args:
            action (str): URL to send recording info
            method (str): HTTP method
            timeout (int): Silence timeout in seconds
            finish_on_key (str): Keys that stop recording
            max_length (int): Maximum length in seconds
            play_beep (bool): Play beep before recording
            trim (str): Trim silence ('trim-silence', 'do-not-trim')
            recording_status_callback (str): Recording status callback URL
            recording_status_callback_method (str): Recording status callback method
            recording_status_callback_event (List[str]): Recording status events
            transcribe (bool): Enable transcription
            transcribe_callback (str): Transcription callback URL
            
        Returns:
            VoiceResponse: Self for method chaining
        """
        record_elem = SubElement(self.root, 'Record')
        
        if action:
            record_elem.set('action', action)
        if method != 'POST':
            record_elem.set('method', method)
        if timeout != 5:
            record_elem.set('timeout', str(timeout))
        if finish_on_key != '1234567890*#':
            record_elem.set('finishOnKey', finish_on_key)
        if max_length != 3600:
            record_elem.set('maxLength', str(max_length))
        if not play_beep:
            record_elem.set('playBeep', 'false')
        if trim != 'trim-silence':
            record_elem.set('trim', trim)
        if recording_status_callback:
            record_elem.set('recordingStatusCallback', recording_status_callback)
        if recording_status_callback_method != 'POST':
            record_elem.set('recordingStatusCallbackMethod', recording_status_callback_method)
        if recording_status_callback_event:
            record_elem.set('recordingStatusCallbackEvent', ' '.join(recording_status_callback_event))
        if transcribe:
            record_elem.set('transcribe', 'true')
        if transcribe_callback:
            record_elem.set('transcribeCallback', transcribe_callback)
        
        return self
    
    def pause(self, length: int = 1) -> 'VoiceResponse':
        """
        Add Pause verb for silence
        
        Args:
            length (int): Pause duration in seconds
            
        Returns:
            VoiceResponse: Self for method chaining
        """
        pause_elem = SubElement(self.root, 'Pause')
        if length != 1:
            pause_elem.set('length', str(length))
        
        return self
    
    def hangup(self) -> 'VoiceResponse':
        """
        Add Hangup verb to end call
        
        Returns:
            VoiceResponse: Self for method chaining
        """
        # Context-aware: make direct API call if possible
        if self._call_sid and self._client:
            try:
                self._client.request('POST', '/hangup', data={'callId': self._call_sid})
            except:
                pass  # Fallback to TwiML
        
        SubElement(self.root, 'Hangup')
        return self
    
    def redirect(self, url: str, method: str = 'POST') -> 'VoiceResponse':
        """
        Add Redirect verb to transfer control
        
        Args:
            url (str): URL to redirect to
            method (str): HTTP method
            
        Returns:
            VoiceResponse: Self for method chaining
        """
        redirect_elem = SubElement(self.root, 'Redirect')
        if method != 'POST':
            redirect_elem.set('method', method)
        redirect_elem.text = url
        
        return self
    
    def reject(self, reason: str = 'rejected') -> 'VoiceResponse':
        """
        Add Reject verb to reject call
        
        Args:
            reason (str): Rejection reason ('rejected', 'busy')
            
        Returns:
            VoiceResponse: Self for method chaining
        """
        reject_elem = SubElement(self.root, 'Reject')
        if reason != 'rejected':
            reject_elem.set('reason', reason)
        
        return self
    
    def append(self, twiml) -> 'VoiceResponse':
        """
        Append another TwiML element
        
        Args:
            twiml: TwiML element to append
            
        Returns:
            VoiceResponse: Self for method chaining
        """
        if hasattr(twiml, 'root'):
            for child in twiml.root:
                self.root.append(child)
        
        return self


class Gather:
    """
    Gather class for nesting verbs inside Gather element
    100% compatible with Twilio's Gather nesting
    """
    
    def __init__(self, gather_element, call_sid: str = None, client = None):
        self.gather_element = gather_element
        self._call_sid = call_sid
        self._client = client
    
    def say(self, message: str, voice: str = None, language: str = None, loop: int = 1) -> 'Gather':
        """
        Add Say verb to Gather
        
        Args:
            message (str): Text to speak
            voice (str): Voice to use
            language (str): Language code
            loop (int): Number of loops
            
        Returns:
            Gather: Self for method chaining
        """
        # Context-aware: make direct API call if possible
        if self._call_sid and self._client:
            try:
                self._client.request('POST', '/gather', data={
                    'callId': self._call_sid,
                    'text': message,
                    'numDigits': int(self.gather_element.get('numDigits', '1')),
                    'timeout': int(self.gather_element.get('timeout', '5')) * 1000,
                    'playTo': 'bridge'
                })
            except:
                pass  # Fallback to TwiML
        
        # Add to TwiML
        say_elem = SubElement(self.gather_element, 'Say')
        if voice:
            say_elem.set('voice', voice)
        if language:
            say_elem.set('language', language)
        if loop != 1:
            say_elem.set('loop', str(loop))
        say_elem.text = message
        
        return self
    
    def play(self, url: str, loop: int = 1, digits: str = None) -> 'Gather':
        """
        Add Play verb to Gather
        
        Args:
            url (str): Audio file URL
            loop (int): Number of loops
            digits (str): DTMF digits
            
        Returns:
            Gather: Self for method chaining
        """
        play_elem = SubElement(self.gather_element, 'Play')
        if loop != 1:
            play_elem.set('loop', str(loop))
        if digits:
            play_elem.set('digits', digits)
        play_elem.text = url
        
        return self
    
    def pause(self, length: int = 1) -> 'Gather':
        """
        Add Pause verb to Gather
        
        Args:
            length (int): Pause duration in seconds
            
        Returns:
            Gather: Self for method chaining
        """
        pause_elem = SubElement(self.gather_element, 'Pause')
        if length != 1:
            pause_elem.set('length', str(length))
        
        return self
