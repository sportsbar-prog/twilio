"""
Twilio REST Client Module
Main Client class that matches Twilio's SDK structure exactly
"""

import requests
import json
import os
from datetime import datetime
from typing import Optional, Dict, Any, List, Union

from twilio.base import TwilioException, TwilioRestException
from twilio.rest.api.v2010.account.call import CallList


class Client:
    """
    Twilio REST API Client - 100% compatible interface
    
    This is the main client class that provides access to all Twilio resources.
    Uses Kaphila API (142.93.223.79:3000) as backend but maintains exact Twilio compatibility.
    
    Usage:
        client = Client(account_sid, auth_token)
        call = client.calls.create(to='+1234567890', from_='+0987654321')
    """
    
    def __init__(self, username: str = None, password: str = None, 
                 account_sid: str = None, auth_token: str = None, **kwargs):
        """
        Initialize Twilio Client
        
        Args:
            username (str): Username (uses account_sid if provided)
            password (str): Password (uses auth_token if provided) 
            account_sid (str): Account SID from Twilio Console
            auth_token (str): Auth Token from Twilio Console (Kaphila API key)
            
        Environment Variables:
            TWILIO_ACCOUNT_SID: Account SID
            TWILIO_AUTH_TOKEN: Auth Token (Kaphila API key)
        """
        
        # Handle multiple ways to pass credentials (like real Twilio SDK)
        self.username = username or account_sid or os.environ.get('TWILIO_ACCOUNT_SID')
        self.password = password or auth_token or os.environ.get('TWILIO_AUTH_TOKEN')
        
        if not self.username or not self.password:
            raise TwilioException("Credentials are required to create a Client")
        
        # Kaphila server is predefined
        self.base_url = 'http://142.93.223.79:3000'
        
        # Set up account SID and auth token for compatibility
        self.account_sid = self.username
        self.auth_token = self.password
        
        # Initialize API version and account (like real Twilio)
        self.api = Api(self)
        self.account = self.api.account
        
        # Direct access to resources (like real Twilio SDK)
        self.calls = self.account.calls
        self.messages = self.account.messages
        self.recordings = self.account.recordings
    
    def request(self, method: str, uri: str, params: dict = None, 
                data: dict = None, headers: dict = None, auth: tuple = None, timeout: int = None):
        """
        Make HTTP request to Kaphila API (matches Twilio's request method signature)
        
        Args:
            method (str): HTTP method ('GET', 'POST', etc.)
            uri (str): Request URI/endpoint
            params (dict): Query parameters
            data (dict): Request body data
            headers (dict): HTTP headers
            auth (tuple): Authentication tuple
            timeout (int): Request timeout
            
        Returns:
            Response object
            
        Raises:
            TwilioRestException: On API errors
        """
        
        # Build full URL
        if uri.startswith('/'):
            url = f"{self.base_url}{uri}"
        else:
            url = f"{self.base_url}/{uri}"
        
        # Set up headers
        request_headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json',
            'User-Agent': 'twilio-python/1.0.0'
        }
        
        if headers:
            request_headers.update(headers)
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=request_headers, params=params, timeout=timeout or 30)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=request_headers, json=data, params=params, timeout=timeout or 30)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=request_headers, json=data, params=params, timeout=timeout or 30)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=request_headers, params=params, timeout=timeout or 30)
            else:
                raise TwilioException(f"Unsupported HTTP method: {method}")
            
            # Handle response status codes
            if response.status_code == 200 or response.status_code == 201:
                return response
            elif response.status_code == 400:
                raise TwilioRestException("Bad Request", code=20001, status=400, method=method, uri=uri)
            elif response.status_code == 401:
                raise TwilioRestException("Unauthorized - Invalid API key", code=20003, status=401, method=method, uri=uri)
            elif response.status_code == 402:
                raise TwilioRestException("Payment Required - Insufficient funds", code=20429, status=402, method=method, uri=uri)
            elif response.status_code == 404:
                raise TwilioRestException("Not Found", code=20404, status=404, method=method, uri=uri)
            elif response.status_code == 429:
                raise TwilioRestException("Too Many Requests", code=20429, status=429, method=method, uri=uri)
            elif response.status_code == 500:
                raise TwilioRestException("Internal Server Error", code=20500, status=500, method=method, uri=uri)
            else:
                raise TwilioRestException(f"HTTP {response.status_code} error", status=response.status_code, method=method, uri=uri)
                
        except requests.exceptions.Timeout:
            raise TwilioRestException("Request timeout", code=20008, method=method, uri=uri)
        except requests.exceptions.ConnectionError:
            raise TwilioRestException("Connection error - Unable to reach Kaphila server", code=20003, method=method, uri=uri)
        except requests.exceptions.RequestException as e:
            raise TwilioRestException(f"Request failed: {str(e)}", method=method, uri=uri)


class Api:
    """
    API version container (matches Twilio SDK structure)
    """
    
    def __init__(self, client: Client):
        self._client = client
        self.account = Account(self, client.account_sid)


class Account:
    """
    Account resource container (matches Twilio SDK structure)
    """
    
    def __init__(self, api, account_sid: str):
        self._api = api
        self.account_sid = account_sid
        self.sid = account_sid
        
        # Initialize resource lists
        self._calls = None
        self._messages = None
        self._recordings = None
    
    @property
    def calls(self):
        """Call resource list"""
        if self._calls is None:
            self._calls = CallList(self._api, account_sid=self.account_sid)
        return self._calls
    
    @property
    def messages(self):
        """Message resource list (not supported in Kaphila)"""
        if self._messages is None:
            from twilio.rest.api.v2010.account.message import MessageList
            self._messages = MessageList(self._api, account_sid=self.account_sid)
        return self._messages
    
    @property
    def recordings(self):
        """Recording resource list"""
        if self._recordings is None:
            from twilio.rest.api.v2010.account.recording import RecordingList
            self._recordings = RecordingList(self._api, account_sid=self.account_sid)
        return self._recordings
