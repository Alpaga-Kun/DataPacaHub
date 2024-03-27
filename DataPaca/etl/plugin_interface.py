from abc import ABC, abstractmethod

class ExtractInterface(ABC):
    @abstractmethod
    def extract(self, params):
        pass

class TransformInterface(ABC):
    @abstractmethod
    def transform(self, data):
        pass

class LoadInterface(ABC):
    @abstractmethod
    def load(self, data):
        pass
