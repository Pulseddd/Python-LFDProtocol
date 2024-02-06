# Python-LFDProtocol
 A "Protocol" to download large file by downloading certain parts of a file and then combining it at the end, like how IDM does.
 (LFD stands for LargeFileDownload btw, yeah its cringe i know) lemme know what i should change it to
### Example:
```python
import LFDProtocol

url = "your_file_url"

protocol = LFDProtocol.File(
    url,
    #_threads = LFDProtocol.DownloadThreads.ULTRA_THREADS (Thread amount can be chosen from DownloadThreads enum. It supports 100 at max in the TOO_MUCH_THREADS enum element).
)
protocol.download()
```
