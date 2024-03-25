 # Build the wheel

pip install -r requirements.txt --break-system-packages
pip install wheel  # Install wheel if you haven't already  # Download PyAudio source distribution
tar -xvf PyAudio-0.2.14.tar.gz  # Extract the source files
cd PyAudio-0.2.14  # Navigate to the extracted directory
python setup.py bdist_wheel --plat-name=manylinux1_x86_64
