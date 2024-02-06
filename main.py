import LFDProtocol, os
from icecream import ic

os.system("cls")

#ic(LFDProtocol.misc.length_to_readable(500000000000000))


url = "https://raw.githubusercontent.com/DosX-dev/MemCleaner/main/source/MemCleaner.c"

protocol = LFDProtocol.File(
    url,
    "MemCleaner.c"
)
protocol.download()