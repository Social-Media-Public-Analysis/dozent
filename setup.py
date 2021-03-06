from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'dozent',
  packages = ['dozent'],
  version = '1.0.2',
  license='GNU-3',
  description = 'Dozent is a powerful downloader that is used to download a ton of twitter data from the internet archive.',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Ali Abbas, Eric Burt, Keelin Becker-Wheeler',
  author_email = 'socialmediapublicanalysis@gmail.com',
  url = 'https://github.com/Social-Media-Public-Analysis/dozent',
  package_data={
        '': ['*.json'],
  },
  download_url = 'https://github.com/Social-Media-Public-Analysis/dozent/releases/tag/v1.0.2',
  keywords = ['TWITTER', 'SCRAPER', 'TWEET'],
  install_requires=[
            'pySmartDL',
            'aria2p',
            'pytest',
            'pyfiglet',
            'numpy',
            'humanize'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9',
  ],
)
