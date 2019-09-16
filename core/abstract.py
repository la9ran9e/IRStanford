from abc import ABC, abstractmethod
from typing import Set, Any, BinaryIO

from .typing import OffsetT


class SimpleIndexT(ABC):
    @abstractmethod
    def feed(self, file: BinaryIO): ...

    @abstractmethod
    def search(self, obj: Any) -> Set[OffsetT]: ...

    @abstractmethod
    def cleanup(self): ...


class MapDocT(ABC):
    @property
    @abstractmethod
    def field(self) -> str: ...

    @field.setter
    @abstractmethod
    def field(self, val): ...


class ProcessingT(ABC):
    @abstractmethod
    def process(self, doc: dict, offset: OffsetT): ...


class PersistentT(ABC):
    @abstractmethod
    def load(self, path): ...

    @abstractmethod
    def dump(self, path): ...


class ProcessingMapDocPersistentIndexT(SimpleIndexT, MapDocT, ProcessingT, PersistentT):
    ...
