import json
import requests
from datetime import datetime
from typing import Dict, Any

def validate_request_data(data: Dict[str, Any]) -> bool:
    """
    Validate the request data.

    Param data: Request data dictionary
    Return: True if the request data is valid, False otherwise
    """
    # Implement validation logic here
    return True

def append_low_prob_tag(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Append "low_prob" tag to "tags" list if the "prob" field is less than 0.25.

    Param data: Request data dictionary
    Return: Request data dictionary with updated "tags" list
    """
    for pred in data['data']['preds']:
        if pred['prob'] < 0.25:
            pred['tags'].append('low_prob')
    return data

def send_message_to_queue(data: Dict[str, Any]) -> bool:
    """
    Send message to RabbitMQ queue.

    Param data: Request data dictionary
    Return: True if message is successfully sent to the queue, False otherwise
    """
    try:
        message = json.dumps(data).encode('utf-8')
        response = requests.post('http://localhost:15672/api/exchanges/%2f/messages',
                                 auth=('guest', 'guest'),
                                 headers={'content-type': 'application/json'},
                                 data=message)
        if response.status_code == 200:
            return True
    except:
        pass
    return False

def handle_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle incoming request.

    Param request_data: Request data dictionary
    Return: Response data dictionary
    """
    if not validate_request_data(request_data):
        return {'status': 'error', 'message': 'Invalid request data'}
    data = append_low_prob_tag(request_data)
    if not send_message_to_queue(data):
        return {'status': 'error', 'message': 'Failed to send message to the queue'}
    return {'status': 'success', 'message': 'Message successfully sent to the queue'}

if __name__ == '__main__':
    # Example
    request_data = {
        'device_id': 'ABC123',
        'client_id': 'DEF456',
        'created_at': str(datetime.now()),
        'data': {
            'license_id': 'GHI789',
            'preds': [
                {
                    'image_frame': 'base64image1',
                    'prob': 0.5,
                    'tags': ['tag1', 'tag2']
                },
                {
                    'image_frame': 'base64image2',
                    'prob': 0.1,
                    'tags': ['tag3', 'tag4']
                }
            ]
        }
    }
    response = handle_request(request_data)
    print(response)