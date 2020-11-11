# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from Products.PluggableAuthService.interfaces.plugins import IPropertiesPlugin
from Products.PluggableAuthService.interfaces.plugins import IRolesPlugin
from Products.PluggableAuthService.interfaces.plugins import IUserEnumerationPlugin
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveMsalLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ICollectiveMsal(IPropertiesPlugin,
                      IUserEnumerationPlugin,
                      IRolesPlugin,
                      ):
    """interface for Collective Microsoft Azure PAS Auth Plugin."""
