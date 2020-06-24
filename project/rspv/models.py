from mongoengine import *


class ProxyRequest(Document):
    """
    Represents a Proxy Request
    """
    user = StringField()
    ip = StringField()
    createdAt = IntField()
    today = DateField
    raw_data = StringField()

    endpoint = StringField()

    status_code = IntField()


class ServerStatus(Document):
    """
    Represents when the proxy was started / stopped
    """

    STATUS_START = "started"
    STATUS_STOP = "stopped"

    STATUS_CHOICES = (
        (STATUS_START, STATUS_START),
        (STATUS_STOP, STATUS_STOP)
    )

    status = StringField(choices=STATUS_CHOICES)
