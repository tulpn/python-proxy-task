import time
import json
import logging

from http.server import BaseHTTPRequestHandler, HTTPServer

import requests
from mongoengine import *

from .settings import *
from .helper import sign_with_jwt, build_payload, render_status_template, save_server_status, get_proxy_status_details, enqueue_request_log

from .models import ServerStatus

# Setup Logging
_logger = logging.getLogger("console" if DEBUG else "")


class ProxyServer(BaseHTTPRequestHandler):
    server_version = PROXY_SEVER_NAME

    def log_message(self, format, *args):
        """
        Overwrite the default logger to console, to the one we configure via our settings!
        Default configuration includes rotated file log via docker / mounted path
        :param format:
        :param args:
        :return:
        """
        _logger.info("%s - - [%s] %s" % (self.address_string(), self.log_date_time_string(), format % args))

    def do_GET(self):
        """
        Implementation of a /health check via GET Method when requesting the PROXY location
        :return:
        """
        # Create a simple health check
        if self.path == "/health":
            health = {'status': 'ok'}
            self.send_response(200)
            self.send_header("Content-type", "text/json")
            self.end_headers()
            self.wfile.write(bytearray(json.dumps(health), 'UTF-8'))
            return

        if self.path == "/status":
            status_data = get_proxy_status_details()
            html = render_status_template(status_data)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytearray(html, 'UTF-8'))
            return

        # send back 404 for everything else, as nothing is configured
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        """
        Handle POST requests as proxy.

        Create JWT token for data, request to original endpoint and return data to requester
        :return:
        """
        # Gather information from original request and build custom request that we can adjust and send off
        # get the origin ip address
        original_requester_ip = self.client_address[0]

        # get the body from the request, based on the length sent from the header attribute Content-Length
        body = self.rfile.read(int(self.headers.get("Content-Length")))

        # Decode the byte to string and load it via the json module
        data = json.loads(body.decode("utf-8"))

        # check if the user attribute is present, if not we cannot create a "valid" JWT token
        # however, handle the via settings.py if we wnat to drop the request or still forward it
        if DROP_JWT_ERROR:
            if JWT_USER_IDENTIFIER not in data:
                self.send_response(422)
                self.end_headers()
                return

        # build our payload to send off to the real endpoint
        jwt_payload = build_payload(data[JWT_USER_IDENTIFIER])

        # final token
        jwt_token = sign_with_jwt(jwt_payload)

        # set a default data to send back, gets overwritten by requests.json()
        return_data = {}

        # set a default status code, in good will we say everything was ok
        # gets overwritten by exception handling or by the requests.status_code
        endpoint_status_code = 200

        # send off json post via requests module
        try:
            # build our headers to include the JWT token
            headers = {
                'x-my-jwt': jwt_token,
                'X-Forwarded-For': original_requester_ip
                # Add any other relevant headers...
            }
            # get the host we want to contact
            response = requests.post(self.path, headers=headers, json=data)
            # set the return values
            endpoint_status_code = response.status_code
            return_data = response.json()

        except Exception as e:
            # if we have timeouts or other issues, we must handle them here
            # first of all we have an internal error
            endpoint_status_code = 500
            # Return an empty json object, could also be used to forward any other error messages
            return_data = {}

        # Log the proxy action to a database to monitor
        enqueue_request_log({
            'request': {
                "ip": original_requester_ip,
                "datetime": jwt_payload['iat'],
                'today': jwt_payload['payload']['date'],
                "data": data
            },
            "response": {
                "status_code": endpoint_status_code
            },
            'user': jwt_payload['payload']['user'],
            'endpoint': self.path,

        })

        # Sending Response to requester
        # forward the status code from the endpoint
        self.send_response(endpoint_status_code)

        # set headers
        self.send_header("Content-type", "text/json")
        self.end_headers()

        # finally write the return data
        self.wfile.write(bytearray(json.dumps(return_data), "utf-8"))


def run():
    try:
        # Connect to DB
        connect(DB_DATABASE_NAME, host=DB_HOST_NAME, username=DB_USER, password=DB_PASSWORD,
                authentication_source='admin')
    except Exception as e:
        _logger.error("Could not connect to database service")

    # Setup the HTTP Server for listening and using our own ProxyServer Instance
    proxyService = HTTPServer((PROXY_HOST_NAME, PROXY_PORT), ProxyServer)

    # Save that the server started
    save_server_status(ServerStatus.STATUS_START)

    try:
        _logger.info("Server Starts - %s - %s:%s" % (time.asctime(), PROXY_HOST_NAME, PROXY_PORT))
        # It runs forever, until closed by user
        proxyService.serve_forever()
    except KeyboardInterrupt:
        pass

    # Gracefully close the server
    proxyService.server_close()

    _logger.info("Server Stops - %s - %s:%s" % (time.asctime(), PROXY_HOST_NAME, PROXY_PORT))
