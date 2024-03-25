 # Build the wheel
pip install -r requirements.txt --break-system-packages
pip install .
pip install toml && python -c 'import toml; c = toml.load("pyproject.toml"); print("\n".join(c["project"]["dependencies"]))' | pip download -r /dev/stdin  --dest=dest




