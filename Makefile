.PHONY: setup

setup:
	@pythonVersion=$$(python3 --version | cut -d ' ' -f 2); \
	majorVersion=$$(echo $$pythonVersion | cut -d '.' -f 1); \
	minorVersion=$$(echo $$pythonVersion | cut -d '.' -f 2); \
	if [ $$majorVersion -lt 3 ] || { [ $$majorVersion -eq 3 ] && [ $$minorVersion -lt 11 ]; }; then \
		echo "\033[0;31mThis repo is not tested on Python versions <= 3.11. Your version: $$pythonVersion\033[0m"; \
	else \
		echo "\033[0;32mPython version is $$pythonVersion. Continuing with setup...\033[0m"; \
	fi
	@if [ ! -d "data_stack_venv" ]; then \
		echo "📦Creating virtual environment..."; \
		python3 -m venv data_stack_venv; \
	else \
		echo "Virtual environment already exists."; \
	fi
	@echo "📦Activating virtual environment..."
	. data_stack_venv/bin/activate && \
	pip install -r stack/requirements.txt
	@if [ ! -f "dev-keypair" ] && [ ! -f "dev-keypair.pub" ]; then \
		echo "🔐Generating SSH keypair..."; \
		ssh-keygen -f dev-keypair -N ""; \
	else \
		echo "SSH keypair already exists."; \
	fi
