import requests
from .exceptions import *


class SupportsPartialContentProtocol():
    def __init__(self, url: str) -> None:
        self.url = url
        self.supports_partial_content = None
        "Supports 206-PartialContent or not"
        self.content_length: int = None
        self.supports_partialcontent()

    def supports_partialcontent(self):
        "Only gets called on `SupportsPartialContentProtocol.__init__` and will NOT return anything. Use `self.supports_partial_content` instead."
        r = requests.head(
            self.url,
        )
        self.content_length = int(r.headers["content-length"])
        r = requests.get(
            self.url,
            headers = {
                "Range": "bytes=0-1"
            }
        )
        sCode = r.status_code
        supports = True if sCode == 206 else False if sCode == 416 else None
        if supports == None:
            raise UnexpectedResponseError("Request failed. (.status_code != 206 or 416)")
        elif supports == False:
            raise DoesNotSupportPartialContentError("The server does not support PartialContent downloading.")
        elif supports == True:
            self.supports_partial_content = True

class PartialContentProtocol(SupportsPartialContentProtocol):
    def __init__(self, url: str) -> None:
        super().__init__(url)