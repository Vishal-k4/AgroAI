 # Build the wheel
pip install -r requirements.txt --break-system-packages
cd pd
python setup.py build
pip install PyAudio --break-system-packages




