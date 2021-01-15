# -*- coding: utf-8 -*-
"""
Discord Bot-lists-api Service
~~~~~~~~~~~~~~~~~~~
A python wrapper for the top.gg API and koreanbots API.

:license: MIT, see LICENSE for more details.
"""

__title__ = 'DBSkr'
__author__ = 'gunyu1019'
__license__ = 'MIT'
__version__ = '0.1'

from .client import client
from .errors import *
from .model import *
from .http import httpClient
