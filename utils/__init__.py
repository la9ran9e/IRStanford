import math
import time


def updating_stat(func):
    def _wrapper(self, a, b):
        start = time.time()
        res = func(self, a, b)
        elapsed = time.time() - start
        self.stat["time_seq"].append(elapsed)
        self.stat["time_elapsed"] += elapsed
        lena, lenb = len(a), len(b)
        self.stat["length_seq"].extend([lena, lenb])
        min_ = min(lena, lenb)
        max_ = max(lena, lenb)
        total = lena + lenb
        self.stat["total_length"] += total
        if self.stat["min_length"] > min_ or self.stat["min_length"] == 0:
            self.stat["min_length"] = min_
        if self.stat["max_length"] < max_:
            self.stat["max_length"] = max_
        return res
    return _wrapper


class Merge:
    def __init__(self):
        self.stat = {
            "iterations": 0,
            "total_length": 0,
            "max_length": 0,
            "min_length": 0,
            "length_seq": [],
            "time_seq": [],
            "time_elapsed": 0
        }

    @updating_stat
    def merge(self, a, b):
        res = []
        i, j = 0, 0
        while (i < len(a)) and (j < len(b)):
            self.stat["iterations"] += 1
            ida = a[i]
            idb = b[j]
            if ida < idb:
                i += 1
            elif ida > idb:
                j += 1
            else:
                res.append(ida)
                i += 1
                j += 1
        return res

    @updating_stat
    def skip_merge(self, a, b):
        res = []
        i, j = 0, 0
        skip_a = int(math.sqrt(len(a)))
        skip_b = int(math.sqrt(len(b)))

        while (i < len(a)) and (j < len(b)):
            self.stat["iterations"] += 1
            ida = a[i]
            idb = b[j]
            if ida < idb:
                skip = min(skip_a, len(a)-1-i)
                if a[i+skip] <= idb:
                    i += skip
                else:
                    i += 1
            elif ida > idb:
                skip = min(skip_b, len(b)-1-j)
                if b[j+skip] <= ida:
                    j += skip
                else:
                    j += 1
            else:
                res.append(ida)
                i += 1
                j += 1
        return res
