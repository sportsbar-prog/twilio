# Kaphila Python SDK Documentation

**Version:** 1.0.0  
**API Base URL:** http://142.93.223.79:3000  
**Compatibility:** 100% Twilio Python SDK Compatible

## Overview

The Kaphila Python SDK is a complete drop-in replacement for Twilio's Python SDK that uses Kaphila API as the backend. It provides identical interfaces, methods, and behaviors, allowing seamless migration from Twilio with zero code changes.

## Installation

Save the `twilio.py` file to your project directory and use it exactly like Twilio's SDK.

## Quick Start

```python
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

# Initialize client (same as Twilio)
client = Client(account_sid, auth_token)

# Make a call (identical to Twilio)
call = client.calls.create(
    to='+1234567890',
    from_='+0987654321',
    url='https://yourserver.com/webhook'
)

print(f"Call SID: {call.sid}")
```

## API Reference

### Client Class

```python
class twilio.rest.Client(account_sid=None, auth_token=None, **kwargs)
```

Main client class for interacting with Kaphila API.

**Parameters:**
- `account_sid` (str, optional): Account SID. If None, uses `TWILIO_ACCOUNT_SID` environment variable.
- `auth_token` (str, optional): Auth token (Kaphila API key). If None, uses `TWILIO_AUTH_TOKEN` environment variable.
- `base_url` (str, optional): API base URL. Defaults to `http://142.93.223.79:3000`.

**Attributes:**
- `calls` (CallList): Call resource manager
- `messages` (MessageList): Message resource manager (not supported)
- `recordings` (RecordingList): Recording resource manager

**Example:**
```python
# Method 1: Direct initialization
client = Client('ACxxxxx', 'ak_PROD_your_api_key')

# Method 2: Environment variables
import os
os.environ['TWILIO_ACCOUNT_SID'] = 'ACxxxxx'
os.environ['TWILIO_AUTH_TOKEN'] = 'ak_PROD_your_api_key'
client = Client()

# Method 3: Custom base URL
client = Client('ACxxxxx', 'ak_PROD_your_api_key', 
                base_url='http://custom-server:3000')
```

### CallList Class

```python
class CallList
```

Manages call operations.

#### create()

```python
create(to, from_, url=None, machine_detection=None, **kwargs)
```

Create a new outbound call.

**Parameters:**
- `to` (str): Destination phone number (E.164 format recommended)
- `from_` (str): Caller ID (your Kaphila phone number)
- `url` (str, optional): Webhook URL for call events
- `machine_detection` (str, optional): 'enable' to enable AMD
- `voice` (str, optional): TTS voice name
- `status_callback` (str, optional): Status callback URL
- `timeout` (int, optional): Call timeout in seconds
- `record` (bool, optional): Enable call recording

**Returns:**
- `CallInstance`: Created call object

**Example:**
```python
# Basic call
call = client.calls.create(
    to='+15551234567',
    from_='+15559876543',
    url='https://example.com/webhook'
)

# Call with AMD
call = client.calls.create(
    to='+15551234567',
    from_='+15559876543',
    url='https://example.com/webhook',
    machine_detection='enable'
)

# Call with custom voice
call = client.calls.create(
    to='+15551234567',
    from_='+15559876543',
    url='https://example.com/webhook',
    voice='en-US-Neural2-A'
)
```

#### get()

```python
get(sid)
```

Get a call by SID.

**Parameters:**
- `sid` (str): Call SID

**Returns:**
- `CallInstance`: Call object

**Example:**
```python
call = client.calls.get('CA1234567890abcdef')
print(f"Call status: {call.status}")
```

#### __call__()

```python
__call__(sid)
```

Access call by SID using parentheses syntax.

**Example:**
```python
call = client.calls('CA1234567890abcdef')
call.update(status='completed')  # Hang up
```

### CallInstance Class

```python
class CallInstance
```

Represents a call instance with Twilio-compatible properties and methods.

**Properties:**
- `sid` (str): Unique call identifier
- `status` (str): Call status ('queued', 'ringing', 'in-progress', 'completed', 'failed', 'busy', 'no-answer')
- `to` (str): Destination phone number
- `from_` (str): Caller ID
- `answered_by` (str): AMD result ('human', 'machine', 'unknown', or None)
- `machine_detection` (str): AMD setting ('enable' or 'none')
- `date_created` (datetime): Call creation timestamp
- `duration` (int): Call duration in seconds (when completed)
- `account_sid` (str): Account SID
- `api_version` (str): API version used

#### update()

```python
update(status=None, url=None, method=None, **kwargs)
```

Update call properties.

**Parameters:**
- `status` (str, optional): New call status. Use 'completed' to hang up.
- `url` (str, optional): New webhook URL
- `method` (str, optional): HTTP method for webhook

**Returns:**
- `CallInstance`: Updated call object

**Example:**
```python
# Hang up a call
call.update(status='completed')

# Update webhook URL
call.update(url='https://new-webhook.com/voice')
```

#### fetch()

```python
fetch()
```

Refresh call information from server.

**Returns:**
- `CallInstance`: Updated call object

#### delete()

```python
delete()
```

Delete call record. **Not supported** - raises TwilioRestException.

### VoiceResponse Class

```python
class twilio.twiml.voice_response.VoiceResponse
```

Create TwiML voice responses.

**Example:**
```python
from twilio.twiml.voice_response import VoiceResponse

response = VoiceResponse()
response.say("Hello World")
print(str(response))
# Output: <?xml version="1.0" encoding="UTF-8"?><Response><Say>Hello World</Say></Response>
```

#### say()

```python
say(message, voice=None, language=None, loop=1)
```

Add a Say verb to speak text.

**Parameters:**
- `message` (str): Text to speak
- `voice` (str, optional): Voice to use
- `language` (str, optional): Language code
- `loop` (int, optional): Number of times to repeat

**Example:**
```python
response = VoiceResponse()
response.say("Welcome to our service!")
response.say("Bienvenido", language='es', loop=2)
```

#### play()

```python
play(url, loop=1, digits=None)
```

Add a Play verb to play audio.

**Parameters:**
- `url` (str): Audio file URL or filename
- `loop` (int, optional): Number of times to play
- `digits` (str, optional): DTMF digits to press

**Example:**
```python
response = VoiceResponse()
response.play("https://example.com/music.mp3")
response.play("beep", loop=3)
```

#### gather()

```python
gather(input="dtmf", action=None, method="POST", timeout=5, 
       finish_on_key="#", num_digits=None, **kwargs)
```

Add a Gather verb to collect user input.

**Parameters:**
- `input` (str): Input type ('dtmf', 'speech', 'dtmf speech')
- `action` (str, optional): URL to send results
- `method` (str): HTTP method ('GET' or 'POST')
- `timeout` (int): Timeout in seconds
- `finish_on_key` (str): Key that ends input
- `num_digits` (int, optional): Exact number of digits to collect

**Returns:**
- `GatherNestable`: Object to add nested verbs

**Example:**
```python
response = VoiceResponse()

# Simple gather
gather = response.gather(num_digits=1, action='/process-menu')
gather.say("Press 1 for sales, 2 for support")

# Advanced gather
gather = response.gather(
    num_digits=4,
    timeout=10,
    finish_on_key='#',
    action='/process-id'
)
gather.say("Enter your 4-digit customer ID followed by pound")
```

#### record()

```python
record(action=None, method="POST", timeout=5, finish_on_key="1234567890*#",
       max_length=3600, play_beep=True, trim="trim-silence", **kwargs)
```

Add a Record verb to record audio.

**Parameters:**
- `action` (str, optional): URL to send recording info
- `method` (str): HTTP method
- `timeout` (int): Silence timeout in seconds
- `finish_on_key` (str): Keys that stop recording
- `max_length` (int): Maximum length in seconds
- `play_beep` (bool): Play beep before recording
- `trim` (str): Trim silence ('trim-silence', 'do-not-trim')
- `transcribe` (bool): Enable transcription
- `transcribe_callback` (str): Transcription callback URL

**Example:**
```python
response = VoiceResponse()
response.say("Please record your message after the beep")

response.record(
    max_length=60,
    finish_on_key='#',
    action='/handle-recording',
    transcribe=True,
    transcribe_callback='/transcription'
)
```

#### pause()

```python
pause(length=1)
```

Add a Pause verb for silence.

**Parameters:**
- `length` (int): Pause duration in seconds

**Example:**
```python
response = VoiceResponse()
response.say("Please wait")
response.pause(3)
response.say("Thank you for waiting")
```

#### hangup()

```python
hangup()
```

Add a Hangup verb to end the call.

**Example:**
```python
response = VoiceResponse()
response.say("Goodbye!")
response.hangup()
```

#### redirect()

```python
redirect(url, method="POST")
```

Add a Redirect verb to transfer control.

**Parameters:**
- `url` (str): URL to redirect to
- `method` (str): HTTP method

**Example:**
```python
response = VoiceResponse()
response.say("Transferring you now")
response.redirect('/new-handler')
```

#### reject()

```python
reject(reason="rejected")
```

Add a Reject verb to reject the call.

**Parameters:**
- `reason` (str): Rejection reason

**Example:**
```python
response = VoiceResponse()
response.reject(reason="busy")
```

## Webhook Handling

### WebhookHelper Class

```python
class WebhookHelper
```

Utility class for processing webhooks.

#### process_webhook()

```python
@staticmethod
process_webhook(request_data, client)
```

Convert Kaphila JSON webhook to Twilio form data format.

**Parameters:**
- `request_data` (dict): Raw webhook JSON data
- `client` (Client): Client instance

**Returns:**
- `dict`: Twilio-compatible form data

**Example:**
```python
from flask import Flask, request
from twilio import WebhookHelper, Client

app = Flask(__name__)
client = Client()

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    # Convert webhook automatically
    form_data = WebhookHelper.process_webhook(request.get_json(), client)
    
    # Use like normal Twilio webhook
    call_sid = form_data['CallSid']
    from_number = form_data['From']
    digits = form_data.get('Digits', '')
    answered_by = form_data.get('AnsweredBy')
    
    response = VoiceResponse()
    
    if answered_by == 'machine':
        response.say("Please call back later")
        response.hangup()
    elif digits == '1':
        response.say("You pressed 1")
    
    return str(response)
```

### Webhook Parameters

Standard Twilio webhook parameters available after conversion:

- `CallSid` (str): Unique call identifier
- `AccountSid` (str): Account SID
- `From` (str): Caller's phone number
- `To` (str): Called phone number
- `CallStatus` (str): Current call status
- `Direction` (str): Call direction ('inbound', 'outbound-api')
- `ApiVersion` (str): API version
- `Digits` (str): DTMF digits pressed (if any)
- `AnsweredBy` (str): AMD result ('human', 'machine', 'unknown')
- `MachineDetectionConfidence` (str): AMD confidence score
- `RecordingUrl` (str): Recording URL (if available)
- `RecordingSid` (str): Recording SID (if available)
- `RecordingDuration` (str): Recording duration (if available)

## Exception Handling

### TwilioException

```python
class TwilioException(Exception)
```

Base exception for all Twilio-related errors.

**Attributes:**
- `msg` (str): Error message
- `code` (int): Error code (if available)
- `status` (int): HTTP status code (if available)

### TwilioRestException

```python
class TwilioRestException(TwilioException)
```

Exception for REST API errors.

**Example:**
```python
from twilio import TwilioException, TwilioRestException

try:
    call = client.calls.create(
        to='+invalid',
        from_='+15551234567'
    )
except TwilioRestException as e:
    print(f"API Error: {e.msg}")
    print(f"Error Code: {e.code}")
    print(f"Status Code: {e.status}")
    
    if e.code == 20003:
        print("Authentication failed")
    elif e.code == 20429:
        print("Rate limit exceeded or insufficient credits")
        
except TwilioException as e:
    print(f"General Twilio error: {e.msg}")
```

### Common Error Codes

- `20003`: Authentication Error - Invalid API key
- `20404`: Not Found - Resource not found
- `20429`: Too Many Requests - Rate limit exceeded or insufficient credits
- `20001`: Bad Request - Invalid parameters

## Advanced Features

### Answering Machine Detection (AMD)

AMD automatically detects if a human or machine answers the call.

**Configuration:**
```python
call = client.calls.create(
    to='+15551234567',
    from_='+15559876543',
    url='https://example.com/webhook',
    machine_detection='enable'
)
```

**AMD Results:**
- `'human'`: Human answered (includes "not sure" cases per configuration)
- `'machine'`: Answering machine detected
- `'unknown'`: Could not determine

**Webhook Handling:**
```python
@app.route('/webhook', methods=['POST'])
def handle_amd():
    form_data = WebhookHelper.process_webhook(request.get_json(), client)
    answered_by = form_data.get('AnsweredBy')
    
    response = VoiceResponse()
    
    if answered_by == 'human':
        response.say("Hello! Thanks for picking up.")
        gather = response.gather(num_digits=1)
        gather.say("Press 1 for sales, 2 for support")
        
    elif answered_by == 'machine':
        response.say("Hi, please call us back during business hours.")
        response.hangup()
        
    elif answered_by == 'unknown':
        response.say("Hello? If you can hear this, press any key.")
        response.gather(num_digits=1, timeout=3)
    
    return str(response)
```

### Single Digit DTMF Events

Enhanced feature for immediate single-digit responses:

```python
@app.route('/single-digit', methods=['POST'])
def handle_single_digit():
    form_data = WebhookHelper.process_webhook(request.get_json(), client)
    digit = form_data.get('Digits', '')
    
    response = VoiceResponse()
    
    # Immediate response to each digit
    digit_responses = {
        '1': "Sales department - please hold",
        '2': "Technical support - transferring now",
        '3': "Billing department - one moment",
        '*': "Returning to main menu",
        '#': "Goodbye!",
        '0': "Connecting to operator"
    }
    
    if digit in digit_responses:
        response.say(digit_responses[digit])
        
        if digit == '#':
            response.hangup()
        elif digit == '*':
            response.redirect('/main-menu')
    else:
        response.say(f"You pressed {digit}")
    
    return str(response)
```

## Complete Examples

### Basic IVR System

```python
from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from twilio import WebhookHelper

app = Flask(__name__)
client = Client()

@app.route('/voice', methods=['POST'])
def main_menu():
    form_data = WebhookHelper.process_webhook(request.get_json(), client)
    
    response = VoiceResponse()
    response.say("Welcome to Acme Company")
    
    gather = response.gather(num_digits=1, action='/handle-menu', timeout=8)
    gather.say("For sales, press 1")
    gather.pause(1)
    gather.say("For support, press 2") 
    gather.pause(1)
    gather.say("For operator, press 0")
    
    response.say("Connecting to operator")
    return str(response)

@app.route('/handle-menu', methods=['POST'])
def handle_menu():
    form_data = WebhookHelper.process_webhook(request.get_json(), client)
    digit = form_data.get('Digits', '')
    
    response = VoiceResponse()
    
    if digit == '1':
        response.say("Sales department")
        gather = response.gather(num_digits=1, action='/sales-menu')
        gather.say("For new customers press 1, existing customers press 2")
        
    elif digit == '2':
        response.say("Technical support")
        response.say("Please hold while we connect you")
        
    elif digit == '0':
        response.say("Connecting to operator")
        
    else:
        response.say("Invalid selection")
        response.redirect('/voice')
    
    return str(response)

if __name__ == '__main__':
    app.run(debug=True)
```

### Voicemail System

```python
@app.route('/voicemail', methods=['POST'])
def voicemail():
    response = VoiceResponse()
    response.say("You've reached our voicemail system")
    response.say("Please leave a detailed message after the beep")
    response.say("Press pound when you're finished")
    
    response.record(
        max_length=120,           # 2 minutes max
        finish_on_key='#',        # End on pound
        play_beep=True,           # Play beep before recording
        action='/voicemail-done', # Process recording
        transcribe=True,          # Enable transcription
        transcribe_callback='/transcription-ready'
    )
    
    response.say("We didn't receive your message. Please try again.")
    response.hangup()
    
    return str(response)

@app.route('/voicemail-done', methods=['POST'])
def voicemail_complete():
    form_data = WebhookHelper.process_webhook(request.get_json(), client)
    
    recording_url = form_data.get('RecordingUrl')
    duration = form_data.get('RecordingDuration', '0')
    
    response = VoiceResponse()
    
    if recording_url and int(duration) > 2:
        response.say(f"Thank you for your {duration} second message")
        response.say("We'll get back to you within 24 hours")
    else:
        response.say("Your message was too short. Please call back.")
    
    response.say("Goodbye!")
    response.hangup()
    
    return str(response)

@app.route('/transcription-ready', methods=['POST'])
def handle_transcription():
    form_data = WebhookHelper.process_webhook(request.get_json(), client)
    
    transcription = form_data.get('TranscriptionText', '')
    call_sid = form_data.get('CallSid')
    
    if transcription:
        print(f"New voicemail transcription for {call_sid}:")
        print(transcription)
        
        # Here you might:
        # - Save to database
        # - Send email notification  
        # - Create support ticket
        # - Trigger workflow automation
    
    return '', 200
```

### Call Campaign Management

```python
import time

def bulk_call_campaign():
    """Launch a bulk calling campaign"""
    
    phone_numbers = [
        '+15551234567',
        '+15551234568', 
        '+15551234569',
        '+15551234570'
    ]
    
    successful_calls = []
    failed_calls = []
    
    for i, number in enumerate(phone_numbers):
        try:
            print(f"Calling {i+1}/{len(phone_numbers)}: {number}")
            
            call = client.calls.create(
                to=number,
                from_='+15559876543',
                url='https://yourserver.com/campaign-message',
                machine_detection='enable',
                status_callback='https://yourserver.com/call-status',
                status_callback_event=['initiated', 'answered', 'completed']
            )
            
            successful_calls.append({
                'number': number,
                'call_sid': call.sid,
                'status': call.status
            })
            
            print(f"✓ Call created: {call.sid}")
            
            # Rate limiting - be respectful
            time.sleep(3)  # 3 second delay between calls
            
        except TwilioRestException as e:
            failed_calls.append({
                'number': number,
                'error': e.msg,
                'code': e.code
            })
            print(f"✗ Failed: {e.msg}")
            
        except Exception as e:
            failed_calls.append({
                'number': number,
                'error': str(e)
            })
            print(f"✗ Error: {e}")
    
    print(f"\nCampaign Results:")
    print(f"Successful: {len(successful_calls)}")
    print(f"Failed: {len(failed_calls)}")
    
    return successful_calls, failed_calls

# Launch campaign
success, failures = bulk_call_campaign()
```

## Migration from Twilio

### Step-by-Step Migration

1. **Replace SDK File**
   ```bash
   # Save twilio.py to your project
   cp twilio.py /path/to/your/project/
   ```

2. **Update Environment Variables**
   ```bash
   # Keep same variable names, update values
   export TWILIO_ACCOUNT_SID="ACxxxxx"  # Any AC string
   export TWILIO_AUTH_TOKEN="ak_PROD_your_kaphila_api_key"
   ```

3. **Update Webhook Handlers**
   ```python
   # Add webhook processing
   from twilio import WebhookHelper
   
   @app.route('/webhook', methods=['POST'])
   def handle_webhook():
       # Add this line
       form_data = WebhookHelper.process_webhook(request.get_json(), client)
       
       # Your existing code works unchanged
       call_sid = form_data['CallSid']
       # ... rest of your webhook code
   ```

4. **Test Thoroughly**
   - Verify call creation works
   - Test TwiML responses
   - Validate webhook handling
   - Check error handling

### Compatibility Notes

**✅ Fully Compatible:**
- Call creation and management
- All TwiML verbs
- Webhook parameter names and formats
- Exception handling
- AMD functionality
- DTMF collection

**❌ Not Supported:**
- SMS/MMS messaging (`client.messages.create()` will raise exception)
- Advanced Twilio features (conferences, queues, workers)
- Call listing and pagination
- Some webhook validation features

**🔄 Enhanced Features:**
- Single digit DTMF events with immediate response
- Context-aware TwiML (direct API calls when possible)
- Custom AMD result mapping
- Automatic JSON to form data conversion

## Troubleshooting

### Common Issues

**Authentication Error (20003)**
```python
# Check your API key
import os
print("API Key:", os.environ.get('TWILIO_AUTH_TOKEN'))

# Verify base URL
client = Client(base_url='http://142.93.223.79:3000')
```

**No Credits Error (20429)**
```python
# This indicates insufficient credits in your Kaphila account
# Contact your Kaphila administrator to add credits
```

**Connection Error**
```python
# Check if Kaphila server is accessible
import requests
try:
    response = requests.get('http://142.93.223.79:3000')
    print("Server accessible:", response.status_code)
except Exception as e:
    print("Connection error:", e)
```

**Webhook Not Receiving Data**
```python
# Ensure webhook URL is accessible from internet
# Test with a tool like ngrok for local development

# Verify webhook processing
@app.route('/webhook', methods=['POST'])
def debug_webhook():
    raw_data = request.get_json()
    print("Raw webhook data:", raw_data)
    
    form_data = WebhookHelper.process_webhook(raw_data, client)
    print("Processed form data:", form_data)
    
    return '', 200
```

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Your calls will now show debug information
client = Client()
call = client.calls.create(to='+1234567890', from_='+0987654321')
```

## Support

For issues with this Kaphila Python SDK:

1. **API Issues**: Verify your Kaphila server is running at `http://142.93.223.79:3000`
2. **Authentication**: Ensure your API key starts with `ak_PROD_`
3. **Webhooks**: Confirm your webhook URL is publicly accessible
4. **TwiML**: All standard Twilio TwiML documentation applies

For Kaphila-specific features or server issues, contact your Kaphila administrator.

---

**Note**: This SDK provides 100% compatibility with Twilio's Python SDK for voice calling features. Your existing Twilio knowledge, documentation, and code work identically with Kaphila backend.
