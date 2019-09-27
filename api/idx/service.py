import os
from typing import Dict

from core.index import Index, Source
from utils import Merge


class Service:
    def __init__(self):
        self._index = Index()
        self._sources: Dict[Source] = dict()

    def get(self, word):
        offsets = self._index.search(word)
        return self._hits(offsets)

    def search(self, query, merge_type="skip_merge"):
        lens = []
        for word in query:
            lens.append((word, len(self._index.search(word))))
        lens.sort(key=lambda x: x[1])

        m = Merge()
        merge_fun = getattr(m, merge_type)
        res = self._index.search(lens[0][0])
        for i in range(1, len(lens)):
            res_ = self._index.search(lens[i][0])
            res = merge_fun(res, res_)

        return self._hits(res), m.stat

    def _hits(self, offsets):
        hits = []
        for offset in offsets:
            hit = dict()
            hit['offset'] = offset
            for key, src in self._sources.items():
                hit[key] = src.search(offset)
            hits.append(hit)
        return hits

    def feed(self, field, file):
        self._index.field = field
        self._index.feed(file)

    def feed_src(self, src, path, format=None):
        if src not in self._sources:
            self._sources[src] = Source(format=format)

        self._sources[src].feed(path)


def prepare_idx(idx: Service, docs, src, prefix='../dataset',
                field='cardHeader__headerDescriptionText'):
    for key, info  in src.items():
        format = info.get('format', None)
        for dataset in info['vals']:
            path = os.path.join(prefix, dataset)
            idx.feed_src(key, path, format=format)

    for dataset in docs:
        path = os.path.join(prefix, dataset)
        with open(path, 'rb') as file:
            idx.feed(field, file)
