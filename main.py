import LFDProtocol, os
from icecream import ic

os.system("cls")

#ic(LFDProtocol.misc.length_to_readable(500000000000000))


content_length = LFDProtocol.protocols.PartialContentProtocol("https://server13.mp3quran.net/basit_mjwd/002.mp3").content_length
thread_amt = 20
a: list = ic(LFDProtocol.misc.divide_ranges(content_length, thread_amt))
ic(LFDProtocol.misc.length_to_readable(content_length))