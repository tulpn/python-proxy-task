import secrets
import logging
from datetime import timezone, datetime
from io import StringIO

import jwt
from mako.lookup import TemplateLookup
from mako.runtime import Context
from redis import Redis
from rq import Queue

from .settings import *
from .tasks import save_request
from .models import ServerStatus, ProxyRequest

_logger = logging.getLogger("console")

# Setup Queue
q = Queue(connection=Redis(host='redis', db=1))


def enqueue_request_log(data):
    """
    Enqueue request data
    :param data: dict
    """
    try:
        q.enqueue(
            save_request, data)
    except Exception as e:
        _logger.error(e)


def get_proxy_status_details():
    """
    Gathers information about the proxy
    :return: dict
    """
    latest_server_status = ServerStatus.objects.order_by('-id').first()
    count_requests = ProxyRequest.objects.count()

    return {
        "latest_server_status": latest_server_status.id.generation_time,
        "count_requests": count_requests,
    }


def save_server_status(status):
    """
    Creates a document in the DB when the server starts
    :param status: str
    """
    server_status = ServerStatus(status=status)
    server_status.save()


def render_status_template(context):
    """
    Returns the parsed template from Mako to show various information
    :param context: dict
    :return: str
    """
    return serve_template("status.html", context)


def serve_template(templatename, context):
    """
    Parse a template file with context data
    :param templatename: str
    :param context: dict
    :return: byte
    """
    template_lookup = TemplateLookup(directories=['{}/templates'.format(ROOT_DIR)])
    template = template_lookup.get_template(templatename)
    buf = StringIO()
    ctx = Context(buf, data=context)
    template.render_context(ctx)
    return buf.getvalue()


def sign_with_jwt(data):
    """
    Sign Data Object and return jwt token string
    :param data: dict
    :return: byte
    """
    return jwt.encode(data, JWT_SECRET, algorithm=JWT_HASH_METHOD)


def build_payload(user):
    """
    Create a payload that is parsed by the JWT method, to create a token for the header
    :param user: str
    :return: dict
    """
    todays_date = datetime.now(tz=timezone.utc).strftime('%Y-%m-%d')
    iat = int(datetime.now(tz=timezone.utc).timestamp())
    return {
        "iat": iat,
        "jti": secrets.token_hex(32),
        'payload': {
            "user": user,
            "date": todays_date
        }
    }
