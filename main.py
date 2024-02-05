import LFDProtocol
from icecream import ic

s = LFDProtocol.SupportsPartialContentProtocol("https://server13.mp3quran.net/basit_mjwd/018.mp3")
ic(s.supports_partial_content)
ic(s.content_length)
