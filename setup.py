import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


what_python = float(sys.version[:3])
print(what_python)

if what_python >= 3.7:
    print("Installing packages for python 3.7 and up")
    install('customtkinter==5.0.3')
    install('requests==2.28.1')
    install('urllib3==1.26.12')
else:
    print("Installing packages for up to python 3.6.9")
    install('requests==2.27.1')
    install('urllib3==1.26.12')
