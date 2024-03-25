 # Build the wheel

pip install -r requirements.txt --break-system-packages
pip install pip-tools
python -m piptools compile \
    -o requirements.txt \
    pyproject.toml
