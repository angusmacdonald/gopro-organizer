try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'GoPro Organizer',
    'author': 'Angus Macdonald',
    'url': 'https://github.com/angusmacdonald/gopro-organizer',
    'download_url': 'http://github.com/angusmacdonald/gopro-organizer',
    'author_email': 'angus.d.macdonald AT gmail.com',
    'version': '0.1',
    'install_requires': ['nose', 'configobj'],
    'packages': ['goproorg'],
    'scripts': [],
    'name': 'goproorg'
}

setup(**config)
