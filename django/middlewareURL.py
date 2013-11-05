__author__ = 'rfoucher'

import backend.urls
from django.conf import settings
from django.utils import six
from django.utils.importlib import import_module
import imp

import logging
logger = logging.getLogger(__name__)


class UrlMiddleware(object):
    """
    Middleware to set up URLs for the backend application
    """

    def __init__(self):
        self._urlconfs = {}

    def process_request(self, request):
        urlconf = getattr(request, 'urlconf', settings.ROOT_URLCONF)
        if isinstance(urlconf, six.string_types):
            urlconf = import_module(getattr(request, 'urlconf', settings.ROOT_URLCONF))
            if urlconf not in self._urlconfs:
                new_urlconf = imp.new_module('urlconf')
                new_urlconf.urlpatterns = (backend.urls.urlpatterns +
                                           list(urlconf.urlpatterns))

                if hasattr(urlconf, 'handler403'):
                    new_urlconf.handler403 = urlconf.handler403
                if hasattr(urlconf, 'handler404'):
                    new_urlconf.handler404 = urlconf.handler404
                if hasattr(urlconf, 'handler500'):
                    new_urlconf.handler500 = urlconf.handler500

                self._urlconfs[urlconf] = new_urlconf
            request.urlconf = self._urlconfs[urlconf]
