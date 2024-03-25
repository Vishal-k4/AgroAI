pip install wheel  # Install wheel if you haven't already  # Download PyAudio source distribution
tar -xvf PyAudio-x.y.z.tar.gz  # Extract the source files
cd PyAudio-x.y.z  # Navigate to the extracted directory
python setup.py bdist_wheel --plat-name=manylinux1_x86_64  # Build the wheel

pip install -r requirements.txt --break-system-packages

