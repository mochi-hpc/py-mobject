from distutils.core import setup
from distutils.extension import Extension
from distutils.sysconfig import get_config_vars
import pkgconfig
import os
import os.path
import sys

(opt,) = get_config_vars('OPT')
os.environ['OPT'] = " ".join(
		    flag for flag in opt.split() if flag != '-Wstrict-prototypes'
		)

server_libs = ['boost_python']
server_libs += pkgconfig.parse('mobject-server')['libraries']
pymobject_server_module = Extension('_pymobjectserver', ["pymobject/src/server.cpp"],
		           libraries=server_libs,
			   include_dirs=['.'],
			   depends=[])

setup(name='pymobject',
      version='0.1',
      author='Matthieu Dorier',
      description="""Python binding for Mobject""",      
      ext_modules=[ pymobject_server_module ],
      packages=['pymobject']
     )
