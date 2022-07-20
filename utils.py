import base64

class Utils:
    def create_datagram_message( msg_body):
        return base64.b64encode(msg_body)   