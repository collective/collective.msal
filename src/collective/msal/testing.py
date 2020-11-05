# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import collective.msal


class CollectiveMsalLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.msal)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.msal:default')


COLLECTIVE_MSAL_FIXTURE = CollectiveMsalLayer()


COLLECTIVE_MSAL_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_MSAL_FIXTURE,),
    name='CollectiveMsalLayer:IntegrationTesting',
)


COLLECTIVE_MSAL_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_MSAL_FIXTURE,),
    name='CollectiveMsalLayer:FunctionalTesting',
)


COLLECTIVE_MSAL_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_MSAL_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveMsalLayer:AcceptanceTesting',
)
