import json
import logging
from django.views import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class MessengerView(View):
    """
    Base View for handling Facebook Messenger Webhooks.
    Subclass this and override `handle_message`, `handle_postback`, and `handle_echo`.
    """
    verify_token = None
    app_id = None

    def get(self, request, *args, **kwargs):
        """Handle Webhook Verification"""
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        
        if mode == 'subscribe' and token == self.verify_token and challenge:
            return HttpResponse(challenge)
        return HttpResponse('Forbidden', status=403)

    def post(self, request, *args, **kwargs):
        """Handle Incoming Events"""
        try:
            body = json.loads(request.body.decode('utf-8'))
            if body.get('object') == 'page':
                for entry in body.get('entry', []):
                    for event in entry.get('messaging', []):
                        self.process_event(event)

                return HttpResponse('EVENT_RECEIVED')
            return HttpResponse('NotFound', status=404)
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return HttpResponse('Internal Server Error', status=500)

    def process_event(self, event):
        """Process a single messaging event"""
        sender_id = event['sender']['id']
        recipient_id = event['recipient']['id']
        is_echo = event.get('message', {}).get('is_echo')
        app_id = event.get('message', {}).get('app_id')

        # Check App ID
        if self.app_id and recipient_id != self.app_id:
            return

        metadata = {
            'sender_id': sender_id,
            'recipient_id': recipient_id,
            'is_echo': is_echo,
            'app_id': app_id
        }

        handler_name = None
        payload = None

        supported_events = ['message', 'postback', 'delivery', 'optin', 'read', 'account_linking']

        for e in supported_events:
            if e in event:
                if 'message' in event:
                    if is_echo:
                        handler_name = 'handle_echo'
                    else:
                        handler_name = 'handle_message'
                    payload = event['message']
                else:
                    handler_name = f'handle_{e}'
                    payload = event[e]
                break
            
        if handler_name:
            metadata['payload'] = payload
            getattr(self, handler_name)(metadata)

    def handle_message(self, metadata):
        """Override to handle text/attachment messages"""
        pass

    def handle_postback(self, metadata):
        """Override to handle postbacks"""
        pass

    def handle_echo(self, metadata):
        """Override to handle echo messages (e.g. from Page Inbox or other apps)"""
        pass
