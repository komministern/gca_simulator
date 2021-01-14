"""
Copyright (C) 2021 Oscar Franzén <oscarfranzen@protonmail.com>

This file is part of GCA Simulator.

GCA Simulator is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

GCA Simulator is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with GCA Simulator.  If not, see <https://www.gnu.org/licenses/>.
"""

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

