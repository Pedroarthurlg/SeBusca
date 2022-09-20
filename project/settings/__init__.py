# flake8: noqa
from .environment import *  # isort:skip
from .installed_apps import *  # isort:skip
from .middlewares import *  # isort:skip

import django_heroku

from .assets import *
from .databases import *
from .debug_toolbar import *
from .i18n import *
from .messages import *
from .security import *
from .templates import *

django_heroku.settings(locals())
