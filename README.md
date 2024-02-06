# Python-LFDProtocol
 A "Protocol" to download large file by downloading certain parts of a file and then combining it at the end, like how IDM does.
# Notes
- The protocol works best when it comes to large files, however, lacks performance when it comes to small files. Manual requests/downloads are usually faster than the protocol if it isnt set to `SINGLE_THREAD`
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
