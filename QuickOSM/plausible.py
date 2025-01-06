__copyright__ = 'Copyright 2025, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'

import json
import logging
import os
import platform

from qgis.core import Qgis, QgsNetworkAccessManager
from qgis.PyQt.QtCore import QByteArray, QDateTime, QUrl
from qgis.PyQt.QtNetwork import QNetworkRequest

from QuickOSM.qgis_plugin_tools.tools.version import version

MIN_SECONDS = 3600
ENV_SKIP_STATS = "3LIZ_SKIP_STATS"
PLAUSIBLE_URL_PROD = "https://bourbon.3liz.com/api/event"
LOGGER = logging.getLogger('QuickOSM')

# For testing purpose, to test.
# Similar to QGIS dashboard
# https://feed.qgis.org/metabase/public/dashboard/df81071d-4c75-45b8-a698-97b8649d7228
# We only collect data listed in the list below
# and the country according to IP address.
# The IP is not stored by Plausible Community Edition https://github.com/plausible/analytics
# Plausible is GDPR friendly https://plausible.io/data-policy
# The User-Agent is set by QGIS Desktop itself


def to_bool(input_string: str) -> bool:
    if isinstance(input_string, bool):
        return input_string
    return input_string.lower() in ['true', '1', 't', 'y', 'yes',]


class Plausible:

    def __init__(self):
        """ Constructor. """
        self.previous_date = None

    def request_stat_event(self) -> bool:
        """ Check and make the request if possible. """
        current = QDateTime().currentDateTimeUtc()
        if self._request_stat_event(current):
            if self._send_stat_event():
                self.previous_date = current
                return True
        return False

    def _request_stat_event(self, current: QDateTime) -> bool:
        """ Request to send an event to the API. """
        if to_bool(os.getenv(ENV_SKIP_STATS, False)):
            # Disabled by environment variable
            return False

        if to_bool(os.getenv("CI", False)):
            # If running on CI, do not send stats
            return False

        if version() in ('master', 'dev'):
            return False

        if self.previous_date and self.previous_date.secsTo(current) < MIN_SECONDS:
            # Not more than one request per hour
            # It's done at plugin startup anyway
            return False

        return True

    def _send_stat_event(self) -> bool:
        """ Send stats event to the API. """
        # Qgis.QGIS_VERSION → 3.34.6-Prizren
        # noinspection PyUnresolvedReferences
        qgis_version_full = Qgis.QGIS_VERSION.split('-')[0]
        # qgis_version_full → 3.34.6
        qgis_version_branch = '.'.join(qgis_version_full.split('.')[0:2])
        # qgis_version_branch → 3.34

        python_version_full = platform.python_version()
        # python_version_full → 3.10.12
        python_version_branch = '.'.join(python_version_full.split('.')[0:2])
        # python_version_branch → 3.10

        data = dict({
            "props": {
                # Plugin version
                "plugin-version": version(),
                # QGIS
                "qgis-version-full": qgis_version_full,
                "qgis-version-branch": qgis_version_branch,
                # Python
                "python-version-full": python_version_full,
                "python-version-branch": python_version_branch,
            },
            "url": PLAUSIBLE_URL_PROD,
            "name": "quickosm",
        })

        data["domain"] = "quickosm"

        request = QNetworkRequest()
        # noinspection PyArgumentList
        request.setUrl(QUrl(PLAUSIBLE_URL_PROD))

        # Only turn ON for debug purpose, temporary !
        extra_debug = False
        if extra_debug:
            request.setRawHeader(b"X-Debug-Request", b"true")
            request.setRawHeader(b"X-Forwarded-For", b"127.0.0.1")
        request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json")

        # noinspection PyArgumentList
        QgsNetworkAccessManager.instance().post(request, QByteArray(str.encode(json.dumps(data))))
        return True
