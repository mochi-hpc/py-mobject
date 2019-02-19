from distutils.core import setup
from distutils.extension import Extension
from distutils.sysconfig import get_config_vars
import pybind11
import pkgconfig
import os
import os.path
import sys

def get_pybind11_include():
    path = os.path.dirname(pybind11.__file__)
    return '/'.join(path.split('/')[0:-4] + ['include'])

(opt,) = get_config_vars('OPT')
os.environ['OPT'] = " ".join(
		    flag for flag in opt.split() if flag != '-Wstrict-prototypes'
		)
pk = pkgconfig.parse('mobject-server')
server_libraries = pk['libraries']
server_library_dirs = pk['library_dirs']
server_include_dirs = pk['include_dirs']
server_include_dirs.append(".")
server_include_dirs.append(get_pybind11_include())

pymobject_server_module = Extension('_pymobjectserver', ["pymobject/src/server.cpp"],
        libraries=server_libraries,
        library_dirs=server_library_dirs,
        include_dirs=server_include_dirs,
        extra_compile_args=['-std=c++11'],
        depends=["pymobject/src/server.cpp"])

setup(name='pymobject',
      version='0.1.1',
      author='Matthieu Dorier',
      description="""Python binding for Mobject""",      
      ext_modules=[ pymobject_server_module ],
      packages=['pymobject']
     )
