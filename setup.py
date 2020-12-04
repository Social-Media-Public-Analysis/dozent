from setuptools import setup
setup(
  name = 'dozent',
  packages = ['dozent'],
  version = '0.4',
  license='MIT',
  description = 'Dozent is a powerful downloader that is used to download a ton of twitter data from the internet archive.',
  long_description='README.md',
  long_description_content_type="text/markdown",
  author = 'Ali Abbas, Eric Burt, Keelin Becker-Wheeler',
  author_email = 'eric.burt@protonmail.com',
  url = 'https://github.com/Social-Media-Public-Analysis/dozent',
  download_url = 'https://github.com/Social-Media-Public-Analysis/dozent/archive/v_04.tar.gz',
  keywords = ['TWITTER', 'SCRAPER', 'DOWNLOAD'],
  install_requires=[
            'pySmartDL',
            'aria2p',
            'pytest',
            'pyfiglet',
            'smpamorpheus',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
