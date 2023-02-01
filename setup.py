from setuptools import setup

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name='jenkins_job_status',
    version='0.1.0',
    install_requires=requirements
)