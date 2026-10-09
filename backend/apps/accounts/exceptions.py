from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        custom_data = {
            'success': False,
            'status_code': response.status_code,
            'message': 'An error occurred during request processing.',
            'errors': response.data,
        }
        if isinstance(response.data, dict) and 'detail' in response.data:
            custom_data['message'] = response.data['detail']
        response.data = custom_data
    return response
