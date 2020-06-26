"""
This is a custom client, to easily test the async behaviour of the http proxy service.

It might otherwise be difficult to test 10 or more concurrent requests via Postman, Chrome or other tools.

The GET handling of the http instance serves a status page, within the request for this page has been a time.sleep(1) added.

On concurrent sessions, it takes at least 10 seconds to load the page, while with async development, it should only take
~ 1 second.

The timings are not 100% accurate, but should be a considered a ball figure for the simple test showing concurrent handling.

"""

import time
import urllib.request

from threading import Thread


def make_get_request(url):
    """
    Get the URL to request
    Prints to stdout the status code of the reponse
    :param url: str
    :return:
    """
    try:
        response = urllib.request.urlopen(url)
        print("{}".format(response.code))
    except Exception as e:
        # catchh all
        print(e)


def run(how_many_times=10, url="http://localhost:8000/status"):
    """
    Run the threads X times for URL
    Defaults are 10 Threads, URL=http://localhost:8000/status
    Make sure HTTP Proxy Servie is running
    :param how_many_times: int
    :param url: str
    :return:
    """
    for r in range(how_many_times):
        Thread(target=make_get_request, args=(url,)).start()


if __name__ == "__main__":
    how_many_times = 10  # change to whatever you want to test
    url = "http://localhost:8000/status"
    run(how_many_times, url)
