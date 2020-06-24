import json
import logging

from mongoengine import *

from .models import ProxyRequest
from .settings import *

_logger = logging.getLogger("console")

# Connect to DB
connect(DB_DATABASE_NAME, host=DB_HOST_NAME, username=DB_USER, password=DB_PASSWORD, authentication_source='admin')


def save_request(request_data):
    """
    Calls ODM to save request data in db
    :param request_data:
    :return:
    """

    pr = ProxyRequest()
    pr.today = request_data['request']['today']
    pr.ip = request_data['request']['ip']
    pr.createdAt = request_data['request']['datetime']
    pr.raw_data = json.dumps(request_data['request']['data'])

    pr.status_code = request_data['response']['status_code']

    pr.user = request_data['user']
    pr.endpoint = request_data['endpoint']

    pr.save()

    _logger.info("Saved entry with id {}".format(pr.id))
