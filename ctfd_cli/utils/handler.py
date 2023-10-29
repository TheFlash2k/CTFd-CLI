import requests
from .logger import logger
from enum import Enum

class Mode(Enum):
    GET = requests.get
    POST = requests.post
    PUT = requests.put
    DELETE = requests.delete
    PATCH = requests.patch

class RequestHandler:
    def MakeRequest(mode : Mode, url: str, token, headers: dict = {}, **kwargs):

        if token == None:
            raise Exception("Token is not set. Required for requests.")

        headers["Authorization"] = f"Token {token}"
        headers["Content-Type"] = "application/json"
        headers["User-Agent"] = "CTFd-CLI-v0.1" # Cuz why not..

        try:
            return mode(url, headers=headers, **kwargs)
        except Exception as E:
            logger.error(f"An error occurred when making a request to {url}: {E.__str__()}")