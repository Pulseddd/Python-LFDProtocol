from enum import Enum

class DownloadThreads(Enum):
    SINGLE_THREAD = 1
    DOUBLE_THREADS = 2
    TRIPLE_THREADS = 3
    PENTA_THREADS = 5
    SEPTA_THREADS = 7
    DECA_THREADS = 10
    ICOSA_THREADS = 20
    HIGH_THREADS = 30
    MEGA_THREADS = 40
    ULTRA_THREADS = 50
    TOO_MANY_THREADS = 100

def length_to_readable(size):
    units = [("B", 1), ("KB", 1024), ("MB", 1024 ** 2), ("GB", 1024 ** 3), ("TB", 1024 ** 4), ("PB", 1024 ** 5), ("EB", 1024 ** 6), ("ZB", 1024 ** 7), ("YB", 1024 ** 8), ("BB", 1024 ** 9)]
    for unit, unit_size in units:
        index = units.index((unit, unit_size))
        next = units[index + 1]
        if unit_size < size < next[1]:
            size = size / unit_size
            break
    size_str = f"{size:.2f}{unit}"
    return size_str

def divide_ranges(content_length: int, thread_amt: int):
    ranges = []
    chunk_size = content_length // thread_amt
    chunk: int = None
    for i in range(thread_amt):
        start = i * chunk_size
        if i != thread_amt - 1:
            end = start + chunk_size - 1
        else:
            end = ""
            chunk = content_length - start
        ranges.append(
            {
                "range": f"bytes={start}-{end}"
            }
        )
    return ranges
