from etl.plugin_manager import PluginManager

if __name__ == "__main__":
    manager = PluginManager()
    # Load the plugin configurations from the specified JSON file
    manager.load_plugins_from_config('./config/plugins_config.json')

    # Print out the loaded plugins for verification
    manager.print_plugins()

    # Execute the extraction process
    extracted_data_list = manager.execute_extraction(params=None)

    if extracted_data_list:
        extracted_data = extracted_data_list[0]  # Work with the first extracted dataset
        # Transform the extracted data
        transformed_data = manager.execute_transformation(data=extracted_data)
        print("All data transformed successfully.")

        # Load the transformed data into the database
        manager.execute_loading(data=transformed_data)
        print("All data loaded successfully.")
    else:
        print("No data extracted.")