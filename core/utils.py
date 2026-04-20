import requests
import re
import threading
from django.conf import settings

def send_whatsapp_message(numbers, message):
    """
    Utility function to send WhatsApp messages via BugRicer Notify API.
    Sends the request in a background thread to prevent blocking the main request.
    """
    api_key = getattr(settings, 'WHATSAPP_API_KEY', None)
    if not api_key:
        error_msg = "WHATSAPP_API_KEY not configured in settings."
        print(f"ERROR: {error_msg}")
        return {"error": error_msg}

    # Handle numbers if passed as list
    if isinstance(numbers, list):
        numbers = ",".join(numbers)

    # Sanitize numbers
    sanitized_numbers = "".join([c if c.isdigit() or c == ',' else "" for c in numbers])
    
    api_url = "https://notifyapi.bugricer.com/wapp/api/send"
    params = {
        'apikey': api_key,
        'number': sanitized_numbers,
        'msg': message
    }

    def execute_request():
        print(f"--- [Background] WhatsApp API Request Started ---")
        print(f"Numbers: {sanitized_numbers}")
        try:
            # Increased timeout to 30s to prevent ReadTimeout errors
            response = requests.post(api_url, params=params, timeout=30)
            print(f"--- [Background] WhatsApp Response (Status: {response.status_code}) ---")
            print(f"Body: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"ERROR: [Background] WhatsApp API Connection Failed: {str(e)}")
        except Exception as e:
            print(f"ERROR: [Background] Unexpected WhatsApp Failure: {str(e)}")
        print(f"----------------------------------------------------------")

    # Launch in a background thread so the main view returns immediately
    thread = threading.Thread(target=execute_request)
    thread.daemon = True
    thread.start()

    return {"status": "request_initiated_in_background"}

