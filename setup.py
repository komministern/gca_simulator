try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'GCA Simulator',
    'author': 'Oscar Franzén',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'oscarfranzen@protonmail.se',
    'version': '0.1',
    'install_requires': ['PySide2', 'numpy'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'projectname'
}

setup(**config)

