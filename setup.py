try:
	from setuptools import setup

except ImportError:
	from distutils.core import setup

config = {
    'name': 'Sudo_root CTF framework',
    'author': 'Sudo_root Team',
    'author_email': 'ayouben9@gmail.com',
    #'long_description': 'from a README.md file',
	'description': 'Python modules which provide a suite of useful utilities for CTFs',
	'url': 'URL to get it at',
	'download_url': 'Where to download it',
	'version': '0.1',
	'install_requires': [],
	'packages': ['sudo_root'],#The one used in the directory
	'scripts': []
	#'include_package_data': True/False # We have to add Manifest.in file
	
	#link some cmd_line with function
	#'entry_points': {'console_scripts': ['cmd_line = module:function',],}
}

setup(**config)
