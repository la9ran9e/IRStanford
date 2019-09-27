def merge(a, b):
    res = []
    i, j = 0, 0
    while (i < len(a)) and (j < len(b)):
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
