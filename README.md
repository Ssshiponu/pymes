# pymes

A simple, lightweight Python wrapper for the Facebook Messenger API.

## Installation

No installation command is available yet as this package is not yet published to PyPI. 
Once published, you will be able to install it via pip:

```bash
pip install pymes-api
```

## Usage

### Basic Example

```python
from pymes import MessengerClient, Text, Attachment

# Initialize the client
sender = MessengerClient(page_access_token="YOUR_PAGE_ACCESS_TOKEN")

# Send a text message
sender.send(recipient_id="USER_ID", message=Text("Hello, world!"))

# Send an attachment (Image)
sender.send("USER_ID", Attachment("image", "https://example.com/image.jpg"))

# Mark as seen
sender.send("USER_ID", action="mark_seen")
```

### Supported Message Types

- `Text`: Simple text messages.
- `Attachment`: Images, files, audio, video.
- `QuickReply`: Messages with quick reply buttons.
- `GenericTemplate`: Carousel-like templates with images and buttons.

## Django Support (New)

You can easily handle incoming messages using the `MessengerView`.

```python
# views.py
from pymes.adapter.django import MessengerView

class BotView(MessengerView):
    verify_token = "YOUR_VERIFY_TOKEN"
    app_id = "YOUR_PAGE_ID" # Optional verification

    def handle_message(self, metadata):
        sender_id = metadata['sender_id']
        message = metadata['payload']
        print(f"Message from {sender_id}: {message}")

    # handle any event defining a method with the event name like handle_{event name}
    

# urls.py
from django.urls import path
from .views import BotView

urlpatterns = [
    path("webhook/", BotView.as_view()),
]
```

## Requirements

- Python 3.10+
- `requests` library

## License

MIT License
