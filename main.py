import LFDProtocol, os
from icecream import ic

os.system("cls")

#ic(LFDProtocol.misc.length_to_readable(500000000000000))


content_length = LFDProtocol.protocols.PartialContentProtocol("https://softcomputers.tech/windows-10-ltsc-2021/en-us_windows_10_enterprise_ltsc_2021_x64.iso").content_length
thread_amt = 20
a: list = ic(LFDProtocol.misc.divide_ranges(content_length, thread_amt))
ic(LFDProtocol.misc.length_to_readable(content_length))