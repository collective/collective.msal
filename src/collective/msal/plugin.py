# -*- coding: utf-8 -*-
"""Class: WindowsauthpluginHelper
"""
from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import InitializeClass
from BTrees import OOBTree
from Products.PluggableAuthService.UserPropertySheet import UserPropertySheet
from Products.PluggableAuthService.interfaces import plugins as pas_interfaces
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from collective.msal.interfaces import ICollectiveMsalLayer
from collective.msal.config import logger
from plone import api
from zope.interface import implementer
import msal
import os
import uuid

CLIENT_ID = os.environ.get('CLIENT_ID', '')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET', '')
AUTHORITY = os.environ.get(
    'AUTHORITY', 'https://login.microsoftonline.com/common')
REDIRECT_PATH = os.environ.get('REDIRECT_PATH', 'collective.msal.getAToken')


zmidir = os.path.join(os.path.dirname(__file__), "zmi")


def url_for(code, **kw):
    routes = {'authorized': kw.get('authorized', '/getAToken'),
              'index': '/'}
    return api.portal.get().absolute_url() + routes.get(code, '404')


@implementer(ICollectiveMsalLayer,
             pas_interfaces.IPropertiesPlugin,
             pas_interfaces.IUserEnumerationPlugin,
             pas_interfaces.IRolesPlugin,
             )
class MSALAuthPlugin(BasePlugin):
    """Multi-plugin to do MSAzure authentication

    """
    meta_type = 'Microsoft AZURE PAS Plugin'
    security = ClassSecurityInfo()

    _properties = (
        {
            "id": "CLIENT_ID",
            "label": "CLIENT_ID",
            "type": "string",
            "mode": "w",
        },
        {
            "id": "CLIENT_SECRET",
            "label": "CLIENT_SECRET",
            "type": "string",
            "mode": "w",
        },
        {
            "id": "AUTHORITY",
            "label": "AUTHORITY",
            "type": "string",
            "mode": "w",
        },
        {
            "id": "REDIRECT_PATH",
            "label": "REDIRECT_PATH",
            "type": "string",
            "mode": "w",
        },
        {
            "id": "SCOPE",
            "label": "SCOPE",
            "type": "lines",
            "mode": "w",
        },
        {
            "id": "AUTOGROUPS",
            "label": "Additional Roles to add to this user",
            "type": "lines",
            "mode": "w",
        },

    )

    def __init__(self, id, title=None, **kw):
        self._setId(id)
        self.title = title
        self.CLIENT_ID = CLIENT_ID
        self.CLIENT_SECRET = CLIENT_SECRET
        self.REDIRECT_PATH = REDIRECT_PATH
        self.AUTHORITY = AUTHORITY
        self.SCOPE = [b"User.ReadBasic.All"]
        self.ENDPOINT = b'https://graph.microsoft.com/v1.0/users'
        self.AUTOGROUPS = [b'Member', ]
        self.init_settings()

    @property
    def scope(self):
        """
        """
        return list(map(lambda x: isinstance(x, bytes) and
                        x.decode() or x, self.SCOPE))

    @property
    def autogroups(self):
        """
        """
        return list(map(lambda x: isinstance(x, bytes) and
                        x.decode() or x, self.AUTOGROUPS))

    @security.private
    def is_plugin_active(self, iface):
        pas = self._getPAS()
        ids = pas.plugins.listPluginIds(iface)
        return self.getId() in ids

    def init_settings(self):
        # userid -> userdata
        self._useridentities_by_userid = OOBTree.OOBTree()

        self.session = {}

    def _remember_identity(self, userid, result):
        if userid is None:
            return
        self._useridentities_by_userid[userid] = result
        return result

    def _setupTicket(self, user_id, result):
        """Set up authentication ticket (__ac cookie) with plone.session.

        Only call this when self.create_ticket is True.
        """
        pas = self._getPAS()
        if pas is None:
            return
        if 'session' not in pas:
            return
        self._remember_identity(user_id, result)

        info = pas._verifyUser(pas.plugins, user_id=user_id)
        if info is None:
            logger.debug(
                'No user found matching header. Will not set up session.')
            return
        request = self.REQUEST
        response = request['RESPONSE']
        pas.session._setupSession(user_id, response)
        logger.debug('Done setting up session/ticket for %s' % user_id)

    @security.private
    def enumerateUsers(
        self,
        id=None,
        login=None,
        exact_match=False,
        sort_by=None,
        max_results=None,
        **kw
    ):
        """we implement only exact matches
        """
        pluginid = self.getId()

        ret = list()

        userid = id or login
        if not userid:
            return
        identity = self._useridentities_by_userid.get(userid)
        if identity is None:
            return

        ret.append(
            {
                'id': userid,
                'login': userid,
                'pluginid': pluginid,
            }
        )
        return ret

    @security.private
    def getPropertiesForUser(self, user, request=None):
        default = {}

        user_id = user.getId()

        ob = self._useridentities_by_userid.get(user_id)
        if ob is not None:
            properties = dict(username=ob.get('preferred_username'),
                              email=ob.get('email'),
                              fullname=ob.get('name')
                              )

            psheet = UserPropertySheet(self.getId(),
                                       schema=None,
                                       **properties,
                                       )
            return psheet

        return default

    def _build_msal_app(self, cache=None, authority=None):
        return msal.ConfidentialClientApplication(
            self.CLIENT_ID, authority=authority or self.AUTHORITY,
            client_credential=self.CLIENT_SECRET, token_cache=cache)

    def _load_cache(self,):
        cache = msal.SerializableTokenCache()
        if self.session.get("token_cache"):
            cache.deserialize(self.session["token_cache"])
        return cache

    def _save_cache(self, cache):
        if cache.has_state_changed:
            self.session["token_cache"] = cache.serialize()

    def _build_auth_url(self, authority=None, scopes=None, state=None):
        return self._build_msal_app(authority=authority).get_authorization_request_url(
            scopes or [],
            state=state or str(uuid.uuid4()),
            redirect_uri=url_for("authorized", _external=True, authorized=self.REDIRECT_PATH))

    # ##
    # pas_interfaces.plugins.IRolesPlugin
    #
    def getRolesForPrincipal(self, principal, request=None):
        default = ()
        if self.enumerateUsers(id=principal.getId()):
            return self.autogroups
        return default


InitializeClass(MSALAuthPlugin)
