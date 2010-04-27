from distutils.core import setup
execfile('bueda/bueda_version.py')
long_description = file('README.rst').read()

classifiers = [
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development',
]

setup(name = 'bueda',
      version = __version__,
      description = 'Wrapper for Bueda API',
      long_description = long_description,
      author = 'Bueda',
      author_email = 'support@bueda.com',
      license = 'MIT',
      platforms = ['Any'],
      classifiers = classifiers,
      url = 'http://www.bueda.com',
      packages = ['bueda'],
      )


