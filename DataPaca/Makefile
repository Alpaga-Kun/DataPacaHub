PYTHON = python3
PROJECT_DIR = .
PLUGIN_CONFIG = $(PROJECT_DIR)/config/plugins_config.json
MAIN_FILE = $(PROJECT_DIR)/main.py

run:
	$(PYTHON) $(MAIN_FILE) --config $(PLUGIN_CONFIG)

test:
	pytest

install:
	pip install -r requirements.txt

clean:
	rm -rf .pytest_cache