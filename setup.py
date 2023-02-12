import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


what_python = float(sys.version[:3])

install('urllib3==1.26.12')
install('requests==2.28.1')

if what_python >= 3.7:
    install('customtkinter==5.0.3')
