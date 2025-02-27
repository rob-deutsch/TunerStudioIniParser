from setuptools import setup

setup(name='TsIniParser',
      version='0.1',
      description='A parser for TunerStudio INI files',
      url='https://github.com/adbancroft/TunerStudioIniParser',
      author='adbancroft',
      author_email='13982343+adbancroft@users.noreply.github.com',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Interpreters',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Text Processing',
      ],      
      license='LGPL',
      packages=['TsIniParser'],
      install_requires=[
          'lark-parser',
          'more-itertools'
      ],
      zip_safe=False)