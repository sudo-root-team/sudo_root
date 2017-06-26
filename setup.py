from setuptools import setup
from setuptools import find_packages

from sudo_root import version


config = {
    'name': 'sudo_root',
    'author': 'Sudo_root Team',
    'author_email': 'ayouben9@gmail.com',
    #'long_description': 'from a README.md file',
    'description': 'Python modules which provide a suite of useful utilities for CTFs',
    'url': 'URL to get it at',
    'download_url': 'Where to download it',
    'version': version,
    'install_requires': [],
    'packages': find_packages(),#The one used in the directory
    'scripts': []
    #'include_package_data': True/False # We have to add Manifest.in file
    	
    #link some cmd_line with function
    #'entry_points': {'console_scripts': ['cmd_line = module:function',],}
}

setup(**config)
