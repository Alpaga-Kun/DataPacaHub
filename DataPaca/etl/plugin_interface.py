from abc import ABC, abstractmethod

class PluginInterface(ABC):
    @abstractmethod
    def extract(self, params):
        """Extrait les données de la source."""
        pass

    @abstractmethod
    def transform(self, data):
        """Transforme les données extraites."""
        pass

    @abstractmethod
    def load(self, data):
        """Charge les données transformées dans la destination."""
        pass
