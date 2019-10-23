"""Provide a suite of useful utilities for CTFs"""

from sudo_root.version import __version__

#This line will help the user to import with the use of the module_name (from module_name import THINGS instead of from module_name.file import THINGS)
#from module_name import *
from sudo_root.crypto import *
from sudo_root.misc import *
from sudo_root.forensic import *
from sudo_root.stegano import *


#List of all modules that can be imported from that modules using from module_name import *, this is useful if we use other modules in our module
#You can also add this line in the module files
__all__ = ["crypto", "misc", "hamming", "zxing", "lcg", "keycode", "LSBExtractor"]


version = __version__
