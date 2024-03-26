class PluginManager:
    def __init__(self):
        self.plugins = {}

    def load_plugin(self, plugin_name, plugin_class):
        """Charge et initialise un plugin."""
        if plugin_name not in self.plugins:
            self.plugins[plugin_name] = plugin_class()

    def get_plugin(self, plugin_name):
        """Retourne une instance de plugin par son nom."""
        return self.plugins.get(plugin_name)

    def list_plugins(self):
        """Liste tous les plugins chargés."""
        return list(self.plugins.keys())
