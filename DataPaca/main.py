from etl.plugin_manager import PluginManager
from plugins.datasource_x import DataSourceX

if __name__ == "__main__":
    manager = PluginManager()
    manager.load_plugin('datasource_x', DataSourceX)

    plugin = manager.get_plugin('datasource_x')
    raw_data = plugin.extract(params=None)
    transformed_data = plugin.transform(raw_data)
    plugin.load(transformed_data)

    print(f"Plugins chargés : {manager.list_plugins()}")
