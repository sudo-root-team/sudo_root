import setuptools
import os
#from sudo_root import version


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


requirements = read("requirements.txt").split()

setuptools.setup(
    name="sudo_root",
    version="0.1",#version,
    url="https://github.com/sudo-root-team/sudo_root",
    author="Sudo_root Team",
    author_email="ayouben9@gmail.com",
    description="Library focused on CTF and cyber-security tools",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    keywords="ctf pwn crypto forensic stegano web reverse engineering cyber-security security",
    install_requires=requirements,
    packages=setuptools.find_packages(),
    license="GPLv3"
)
