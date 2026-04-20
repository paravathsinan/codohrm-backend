from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .utils import send_whatsapp_message

class SendWhatsAppView(APIView):
    """
    Proxy view to send WhatsApp messages via BugRicer Notify API.
    Uses the secret API key stored in backend environment variables.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        numbers = request.data.get('numbers')
        message = request.data.get('message')
        
        if not numbers or not message:
            return Response(
                {"error": "Numbers (comma-separated or list) and message are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        response_data = send_whatsapp_message(numbers, message)

        if "error" in response_data:
            # Check if it's a configuration error or a connection error
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            if "not configured" in response_data["error"]:
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            
            return Response(response_data, status=status_code)

        return Response(response_data, status=status.HTTP_200_OK)
