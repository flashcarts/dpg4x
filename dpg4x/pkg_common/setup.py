# This distutil file is used from the real RPM spec file, dpg4x.spec
import glob,os
from distutils.core import setup
setup(name='dpg4x',
      version='2.2',
      license='GPLv3',
      url='http://sourceforge.net/projects/dpg4x',
      description='GUI to encode files into the DPG video format',
      py_modules=[f.replace(".py","") for f in glob.glob("*.py")],
      packages=['moreControls'],
      scripts=[os.path.join('pkg_common', 'dpg4x'),
               os.path.join('pkg_common', 'dpg2avi'),
               os.path.join('pkg_common', 'dpgimginjector')],
      data_files=[('icons', glob.glob(os.path.join('icons', '*.png')))]
      )
