import requests, threading, re

from LFDProtocol import misc
from .exceptions import *
from . import misc
from icecream import ic
ic.prefix = " "

class ServerPartialContentSupport():
    def __init__(self, url: str) -> None:
        self.url = url
        self.supports_partial_content = None
        "Supports 206-PartialContent or not"
        self.content_length: int = None
        self.filename: str = ""
        self.supports_partialcontent()

    def supports_partialcontent(self):
        "Only gets called on `SupportsPartialContentProtocol.__init__` and will NOT return anything. Use `self.supports_partial_content` instead."
        supports = None
        r = requests.head(
            self.url,
            timeout = 999999,
            allow_redirects = True
        )
        self.filename = str(r.headers.get("content-disposition", None)).split("attachment; ")[1].split("filename=")[1]
        ic(self.filename)
        self.content_length = int(r.headers["content-length"])
        r = requests.get(
            self.url,
            headers = {
                "Range": "bytes=0-0"
            },
            stream = True #                                                                                                                                _
        )                                                                                                                                                 # |
        for chunk in r.iter_content(chunk_size = 1024):                                                                                                   # |
            if len(chunk) > 1 and r.status_code == 200:                                                                                                   # | 2nd paragraph in https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Range
                r.close() # server doesnt support PartialContent. Close stream to prevent unwanted downloads & excessive network/data usage                 |
                supports = False                                                                                                                      #    _|
                ic("Stream closed due to lack of PartialContent support")
        
        if not isinstance(supports, bool):
            supports = True if r.status_code == 206 else None
        
        if supports == None:
            if r.status_code == 416:
                raise UnexpectedResponseError("File has no size (0 bytes)")
            raise UnexpectedResponseError(f"Request failed. {r.status_code} (!= 206 or 416)")
        elif supports == False:
            raise DoesNotSupportPartialContentError("The server does not support PartialContent downloading.")
        elif supports == True:
            self.supports_partial_content = True

class PartialContentProtocol(ServerPartialContentSupport):
    def __init__(self, url: str, _threads: misc.DownloadThreads = misc.DownloadThreads.PENTA_THREADS) -> None:
        super().__init__(url)
        self.thread_amt = _threads
        self.estimated_size = misc.length_to_readable(self.content_length)
        self.ranges: list[dict[str, str]] = misc.divide_ranges(self.content_length, self.thread_amt.value)
        self.threads: list[threading.Thread] = []
        self.content: list[tuple[int, bytes]] = []
        self.start_end_regex = r"bytes=(.+)-(.+)"

    def download_content(self):
        estimatedSize = f"Estimated size: ~{self.estimated_size}"
        ic(estimatedSize)
        start, end = re.search(self.start_end_regex, self.ranges[1]['range']).groups()
        estimatedSizePerThread = f"Estimated size per thread: {misc.length_to_readable(int(end) - int(start))}"
        ic(estimatedSizePerThread)
        self.prepare_threads()
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()
        data: bytes = b""
        for _ in range(self.thread_amt.value):
            for i, c in self.content:
                if _ == i:
                    data += c if c else b""
                else: continue
        return data
        
    def prepare_threads(self):
        for i in range(self.thread_amt.value):
            self.threads.append(
                threading.Thread(
                    target = self.thread_target,
                    args = (self.ranges[i], i)
                )
            )

    def thread_target(self, range: dict[str, str], i: int):
        r = requests.get(
            self.url,
            headers = {**range, **{'Accept-Encoding': 'identity'}},
            stream = True
        )
        if r.status_code == 206:
            data = b""
            for chunk in r.iter_content(1024):
                data += chunk
            self.content.append(
                (
                    i,
                    data
                )
            )
            done = f"Thread no. {i} done"
            ic(done)
        elif r.status_code == 200:
            raise DoesNotSupportPartialContentError("Server does not support PartialContent downloading.")
        elif r.status_code == 416:
            raise InvalidRangeError("An error occured while downloading a range of bytes. (Usually an issue in calculation of range chunks)")
        else:
            raise UnexpectedResponseError(f"An unexpected response was recieved: {r.status_code}")
    
class File(PartialContentProtocol):
    def __init__(self, url: str, file_name: str = None, _threads: misc.DownloadThreads = misc.DownloadThreads.ICOSA_THREADS) -> None:
        super().__init__(url, _threads)
        self.file_name = file_name
        self.name_from_contentdisposition = lambda header: re.match(r"filename=(.+)", header) if header else None

    def download(self):
        content = self.download_content()
        ic(self.filename)
        with open(f"{self.file_name if self.file_name else self.filename if self.filename else 'unknown_file'}", "wb") as f:
            f.write(content)
        ic("Finished downloading!")