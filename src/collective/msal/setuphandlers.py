# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from collective.msal import MSALAuthPlugin
from zope.component.hooks import getSite


TITLE = "'Microsoft AZURE PAS Plugin"


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'collective.msal:uninstall',
        ]


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def remove_persistent_import_step(context):
    """Remove broken persistent import step.

    profile/import_steps.xml defined an import step with id
    "pas.plugins.ldap.setup" which pointed to
    pas.plugins.ldap.setuphandlers.setupPlugin.
    This function no longer exists, and the import step is not needed,
    because a post_install handler is now used for this.
    But you get an error in the log whenever you import a profile:

      GenericSetup Step pas.plugins.ldap.setup has an invalid import handler

    So we remove the step.
    """
    registry = context.getImportStepRegistry()
    import_step = "collective.msal.setup"
    if import_step in registry._registered:
        registry.unregisterStep(import_step)


def _addPlugin(pas, pluginid="acl_msal"):
    installed = pas.objectIds()
    if pluginid in installed:
        return TITLE + " already installed."
    plugin = MSALAuthPlugin(pluginid, title=TITLE)
    pas._setObject(pluginid, plugin)
    plugin = pas[plugin.getId()]  # get plugin acquisition wrapped!
    for info in pas.plugins.listPluginTypeInfo():
        interface = info["interface"]
        if not interface.providedBy(plugin):
            continue
        pas.plugins.activatePlugin(interface, plugin.getId())
        pas.plugins.movePluginsDown(
            interface, [x[0]
                        for x in pas.plugins.listPlugins(interface)[:-1]]
        )


def post_install(context):
    site = getSite()
    pas = site.acl_users
    _addPlugin(pas)
