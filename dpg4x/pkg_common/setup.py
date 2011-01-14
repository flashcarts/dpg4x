# This distutil file is used from the real RPM spec file, dpg4x.spec
import glob,os
from distutils.core import setup
setup(name='dpg4x',
      version='2.0',
      license='GPLv3',
      url='http://sourceforge.net/projects/dpg4x',
      description='GUI to encode files into the DPG video format',
      py_modules=[f.replace(".py","") for f in glob.glob("*.py")],
      packages=['moreControls'],
      scripts=[os.path.join('rpm', 'dpg4x'),
               os.path.join('rpm', 'dpg2avi')],
      data_files=[('icons', glob.glob(os.path.join('icons', '*.png')))]
      )
