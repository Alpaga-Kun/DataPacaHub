import os
import json
import importlib


class PluginManager:
    def __init__(self):
        self.plugins = {'extractors': {}, 'transformers': {}, 'loaders': {}}

    def load_plugin(self, plugin_type, plugin_instance, plugin_id):
        """Loads a plugin instance under its type and ID."""
        if plugin_type in self.plugins:
            self.plugins[plugin_type][plugin_id] = plugin_instance

    def load_plugins_from_config(self, config_path):
        with open(config_path, 'r') as file:
            config = json.load(file)

        # Temporary storage for filenames used by extractors
        extractor_filenames = {}

        for plugin_type, plugins in config.items():
            for plugin_info in plugins:
                full_path = plugin_info["class_path"]
                *module_parts, class_name = full_path.split('.')
                module_path = '.'.join(module_parts)

                module = importlib.import_module(module_path)
                plugin_class = getattr(module, class_name)

                if plugin_type == 'extractors':
                    # Store filename for use by loaders
                    extractor_filenames[plugin_info['id']
                                        ] = plugin_info['params']['filename']

                # Dynamically set table name for loaders based on extractor's filename
                if plugin_type == 'loaders':
                    for extractor_id, filename in extractor_filenames.items():
                        base_name = os.path.splitext(
                            os.path.basename(filename))[0]
                        # Update the table name
                        plugin_info['params']['table_name'] = base_name

                plugin_instance = plugin_class(**plugin_info.get('params', {}))
                self.load_plugin(plugin_type, plugin_instance,
                                 plugin_info['id'])

    def execute_extraction(self, params=None):
        extracted_data = []
        for plugin_id, extractor in self.plugins['extractors'].items():
            data = extractor.extract(params)
            extracted_data.append(data)
        return extracted_data

    def execute_transformation(self, data):
        """Executes the transform method for all transformer plugins."""
        for plugin_id, transformer in self.plugins['transformers'].items():
            data = transformer.transform(data)
        return data

    def execute_loading(self, data):
        """Executes the load method for all loader plugins."""
        for plugin_id, loader in self.plugins['loaders'].items():
            loader.load(data)

    def get_plugins(self):
        return self.plugins

    def print_plugins(self):
        for plugin_type, plugins in self.plugins.items():
            print(f"{plugin_type}:")
            for plugin_id, plugin in plugins.items():
                print(f"\t{plugin_id}: {type(plugin).__name__}")
