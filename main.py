import LFDProtocol, os
from icecream import ic

os.system("cls")

#ic(LFDProtocol.misc.length_to_readable(500000000000000))


url = "https://archive.org/download/en-us_windows_10_iot_enterprise_ltsc_2021_x64_dvd_257ad90f_202301/en-us_windows_10_iot_enterprise_ltsc_2021_x64_dvd_257ad90f.iso"

url = "https://github.com/pbatard/rufus/releases/download/v4.4/rufus-4.4p.exe"

protocol = LFDProtocol.File(
    url,
    _threads = LFDProtocol.DownloadThreads.TOO_MANY_THREADS
)
protocol.download()