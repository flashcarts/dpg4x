import glob,os
from setuptools import setup, find_packages

top_directory = "dpg4x"
icon_files=[(os.path.join(top_directory, 'icons'), glob.glob(os.path.join(top_directory, 'icons', '*.png')))]
i18n_files=[(os.path.join(os.path.dirname(f)), [f]) for f in glob.glob(os.path.join(top_directory, 'i18n', '*', 'LC_MESSAGES', 'dpg4x.mo'))]
doc_files = [(os.path.join(top_directory, 'doc'), ['LICENSE', 'CREDITS', 'INSTALL', 'INSTALL.win', 'README', 'ChangeLog'])]

from distutils.core import setup
setup(name='dpg4x',
      version='3.0-alpha',
      license='GPLv3',
      url='http://sourceforge.net/projects/dpg4x',
      description='GUI to encode files into the DPG video format',
      author='d0malaga, mpdavig, xukosky @sourceforge',
      maintainer='Tomas Aronsson ',
      maintainer_email='<d0malaga@users.sourceforge.net>',
      py_modules=['dpg4x_main.py'],
      # py_modules=[f.replace(".py","") for f in glob.glob("*.py")],
      packages=['dpg4x','dpg4x.moreControls'],
      # packages=find_packages()
      data_files= icon_files + i18n_files + doc_files,
      entry_points={
          "console_scripts": [
              "dpg4x_cmd = dpg4x.Dpg4x:main"
          ],
          "gui_scripts": [
              "dpg4x = dpg4x.Dpg4x:main"
          ]
      },
      # TBD: different for Ubuntu, Fedora, Windows... and some non python deps too
      install_requires=["wxPython > 4.0",
                        "pywin32 >= 1.0;platform_system=='Windows'"]
)
