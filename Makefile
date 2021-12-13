# Starts a project
start:
	python main.py

# Loads all models and dependencies
setup: install_dependencies install_models

# Installs python dependencies
install_dependencies:
	pip install transformers || true
	pip uninstall telegram || true
	pip uninstall python-telegram-bot || true
	pip install python-telegram-bot || true

# Installs models directories
install_models:
	python download_models.py || true
