from pymes import MessengerClient, Text, Attachment, Images

sender = MessengerClient(page_access_token="***")

sender.send(recipient_id="***", message=Text("Hello, world!"))
sender.send("***", action="mark_seen")
sender.send("***", Attachment("image", "https://example.com/image.jpg"))
sender.send("***", Images(["https://example.com/image1.jpg", "https://example.com/image2.jpg"]))