from etl.plugin_interface import PluginInterface

class DataSourceX(PluginInterface):
    def extract(self, params):
        print("Extraction de données depuis DataSourceX.")
        return {"data": "données brutes"}

    def transform(self, data):
        print("Transformation des données de DataSourceX.")
        return {"data": "données transformées"}

    def load(self, data):
        print("Chargement des données transformées dans la destination.")
