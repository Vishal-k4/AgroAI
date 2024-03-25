pip install virtualenv

# Create a virtual environment
python -m venv myenv

# Activate the virtual environment
source myenv/bin/activate

pip install -r requirements.txt --break-system-packages
