# -*- coding: utf-8 -*-
"""Init and utils."""
from AccessControl.Permissions import add_user_folders
from Products.PluggableAuthService import registerMultiPlugin
from .plugin import MSALAuthPlugin


def initialize(context):
    registerMultiPlugin(MSALAuthPlugin.meta_type)
    context.registerClass(
        MSALAuthPlugin,
        permission=add_user_folders,
        #icon=os.path.join(zmidir, "ldap.png"),
        #        constructors=(manage_addLDAPPluginForm, manage_addLDAPPlugin),
        visibility=None,
    )
