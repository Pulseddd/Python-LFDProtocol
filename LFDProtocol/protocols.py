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
        supports = None
        r = requests.head(
            self.url,
        )
        self.content_length = int(r.headers["content-length"])
        r = requests.get(
            self.url,
            headers = {
                "Range": "bytes=0-0"
            },
            stream = True #                                                                                                                                _
        )                                                                                                                                                 # |
        for chunk in r.iter_content(chunk_size = 1024):                                                                                                   # |
            if len(chunk) > 1 and r.status_code == 200:                                                                                                                            # | 2nd paragraph in https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Range
                r.close() # server doesnt support PartialContent. Close stream to prevent unwanted downloads & excessive network/data usage                 |
                supports = False                                                                                                                      #    _|
        
        if not isinstance(supports, bool):
            supports = True if r.status_code == 206 else None
        if supports == None:
            if r.status_code == 416:
                raise UnexpectedResponseError("File has no size (0 bytes)")
            raise UnexpectedResponseError("Request failed. (.status_code != 206 or 416)")
        elif supports == False:
            raise DoesNotSupportPartialContentError("The server does not support PartialContent downloading.")
        elif supports == True:
            self.supports_partial_content = True

class PartialContentProtocol(SupportsPartialContentProtocol):
    def __init__(self, url: str) -> None:
        super().__init__(url)