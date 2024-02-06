import LFDProtocol, os, time, requests
from icecream import ic

os.system("cls")

#ic(LFDProtocol.misc.length_to_readable(500000000000000))


url = "https://archive.org/download/en-us_windows_10_iot_enterprise_ltsc_2021_x64_dvd_257ad90f_202301/en-us_windows_10_iot_enterprise_ltsc_2021_x64_dvd_257ad90f.iso"

url = "https://github.com/pbatard/rufus/releases/download/v4.4/rufus-4.4p.exe"
# ^^ ~1.37MB


start = time.time()
r = requests.get(url)
with open("rufus.exe", "wb") as f:
    f.write(r.content)
end = time.time() - start
man = f"Manual took: {end}" # ~2.098s
ic(man)

start = time.time()
protocol = LFDProtocol.File(
    url,
    _threads = LFDProtocol.DownloadThreads.SINGLE_THREAD
)
protocol.download()
end = time.time() - start
prot = f"LFDProtocol took: {end}" # ~5.144s on TOO_MANY_THREADS & 1.906s on SINGLE_THREAD
ic(prot)