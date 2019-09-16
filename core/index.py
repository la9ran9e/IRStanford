import json
from collections import defaultdict

from .abstract import ProcessingMapDocPersistentIndexT, SimpleIndexT, PersistentT
from .typing import OffsetT


class Index(ProcessingMapDocPersistentIndexT):
    def __init__(self, index_path=None):
        self._field = None
        self._offset = 0
        if not index_path:
            self._index = defaultdict(list)
        else:
            self.load(index_path)

    def load(self, path):
        with open(path, 'rb') as f:
            for line in f:
                term = json.loads(line.rstrip())
                self._index[term['term']].extend(term['offsets'])

    @property
    def field(self):
        return self._field

    @field.setter
    def field(self, val):
        self._field = val

    def feed(self, file):
        assert self.field
        for line in file:
            doc = json.loads(line.rstrip())
            self.process(doc, self._offset)
            self._offset += 1

    def dump(self, output):
        with open(output, 'a') as f:
            for term, offsets in self._index.items():
                jterm = json.dumps({'term': term, 'offsets': offsets}, ensure_ascii=False)
                f.write(jterm+'\n')

    def process(self, doc: dict, offset: OffsetT):
        val = doc.get(self.field, None)
        if val is None:
            return
        words = val.split()
        for word in words:
            word = word.lower()
            self._index[word].append(offset)

    def search(self, word):
        if word not in self._index:
            return list()
        return self._index[word]

    def cleanup(self):
        self._field = None
        self._index = defaultdict(set)


class Source(SimpleIndexT, PersistentT):
    def __init__(self, index_path=None):
        self._index = list() if not index_path else self.load(index_path)
        self._files = dict()

    def load(self, path):
        with open(path, 'rb') as f:
            for line in f:
                idx = json.loads(line.rstrip())
                self._index.append((idx['path'], idx['n']))

                if idx['path'] not in self._files:
                    self._files[idx['path']] = open(idx['path'], 'r')

    def feed(self, path):
        self._files[path] = src = open(path, 'r')
        while True:
            if src.readline() == '':
                break
            self._index.append((path, src.tell()))

    def dump(self, path):
        with open(path, 'a') as f:
            for path, n in self._index:
                f.write(json.dumps({'path': path, 'n': n})+'\n')

    def search(self, offset):
        assert self._index
        if offset > len(self._index):
            raise IndexError('Offset out of index')
        path, n = self._index[offset]
        self._files[path].seek(n)
        return self._files[path].readline().strip()

    def cleanup(self):
        self._index = list()
        self._files = dict()
