# -*- coding: utf-8 -*-
"""Global logger used by the server."""
__author__ = "Marten4n6"
__license__ = "GPLv3"

import logging

logging.basicConfig(format="[%(levelname)s] %(filename)s - %(message)s", level=logging.DEBUG)
logging.getLogger("werkzeug").setLevel(logging.WARNING)

log = logging.getLogger(__name__)
