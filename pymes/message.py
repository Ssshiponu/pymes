import json

class Message:
    """Base class for all messages types"""
    def __init__(self):
        pass
    
    def to_dict(self):
        """Returns the dictionary representation of the message"""
        return {}

    def __str__(self):
        """Returns the JSON string representation of the message"""
        return json.dumps(self.to_dict())

class Text(Message):
    """Text message type"""
    def __init__(self, text):
        self.text = text

    def to_dict(self):
        return {"text": self.text}

class Attachment(Message):
    """Attachment message type"""
    def __init__(self, type: str, url: str, is_reusable: bool = False):
        self.type = type
        self.url = url
        self.is_reusable = is_reusable

    def to_dict(self):
        return {
            "attachment": {
                "type": self.type, 
                "payload": {
                    "url": self.url,
                    "is_reusable": self.is_reusable
                }
            }
        }

class QuickReply(Message):
    """Quick reply message type"""
    def __init__(self, text: str, buttons: list[str]):
        if len(buttons) > 13:
            raise ValueError("Quick Reply can have maximum 13 buttons")
        self.text = text
        self.buttons = buttons

    def to_dict(self):
        return {"text": self.text, "quick_replies": self._get_quick_replies()}

    def _get_quick_replies(self):
        return [{"content_type": "text", "title": button, "payload": button.upper().replace(" ", "_")} for button in self.buttons]

class Button:
    """Button for Generic Template"""
    def __init__(self, title: str, type: str = "postback", payload: str | None = None, url: str | None = None):
        self.type = type
        self.title = title
        self.payload = payload
        self.url = url

        if self.type == "web_url" and not self.url:
            raise ValueError("Web URL is required for web_url type")
        if self.type == "postback" and not self.payload:
            raise ValueError("Payload is required for postback type")
    
    def to_dict(self):
        return {"type": self.type, "title": self.title, "payload": self.payload, "url": self.url}


class GenericTemplateElement:   
    """GElement for Generic Template"""
    def __init__(self, title: str, subtitle: str | None = None, image_url: str | None = None, buttons: list[Button] | None = None):
        self.title = title
        self.subtitle = subtitle
        self.image_url = image_url
        self.buttons = buttons or []
    
    def to_dict(self):
        data: dict = {"title": self.title}
        if self.subtitle:
            data["subtitle"] = self.subtitle
        if self.image_url:
            data["image_url"] = self.image_url
        if self.buttons:
            if len(self.buttons) > 3:
                raise ValueError("Generic Template can have maximum 3 buttons") 
            data["buttons"] = [b.to_dict() for b in self.buttons]
        return data

class GenericTemplate(Message):
    """Generic template message type"""
    def __init__(self, elements: list[GenericTemplateElement]):
        if len(elements) > 10:
            raise ValueError("Generic Template can have maximum 10 elements")
        self.elements = elements

    def to_dict(self):
        return {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "image_aspect_ratio": "square",
                    "elements": [e.to_dict() for e in self.elements]
                }
            }
        }
