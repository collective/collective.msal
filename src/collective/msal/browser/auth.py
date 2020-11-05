# -*- coding: utf-8 -*-
from AccessControl import Unauthorized
from Products.Five.browser import BrowserView
from collective.msal.config import MessageFactory as _
from collective.msal.config import logger
from collective.msal.plugin import url_for
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from urllib import parse
from zope.interface import alsoProvides
import uuid


class AuthTokenView(BrowserView):
    """
    """

    def __call__(self,):
        """
        """
        request = self.request
        alsoProvides(request, IDisableCSRFProtection)

        pas = self._getPas()
        acl_msal = pas.get('acl_msal')

        if request.get('code'):
            cache = acl_msal._load_cache()
            result = acl_msal._build_msal_app(cache=cache).acquire_token_by_authorization_code(
                request.get('code'),
                scopes=acl_msal.scope,  # Misspelled scope would cause an HTTP 400 error here
                redirect_uri=url_for("authorized", _external=True, authorized=acl_msal.REDIRECT_PATH))
            if "error" in result:
                raise Unauthorized

            userid = result.get('id_token_claims').get('preferred_username')
            acl_msal._setupTicket(userid, result.get('id_token_claims'))

            acl_msal._save_cache(cache)
        return request.RESPONSE.redirect(self.extractCameFrom(request.HTTP_REFERER))

    def extractCameFrom(self, referer=None):
        default = url_for('index')
        purl = api.portal.get().absolute_url()
        # microsot puo' aver riscritto l'url con un passaggio intermedio
        # recuperiamo il referer dallo state
        state = self.request.get('state')
        try:
            referer = parse.unquote(state.split('|')[-1])
            if purl not in referer:
                # preveniamo l'injection di altri referer
                return default
        except:
            logger.error('referer compromesso. state: {}'.format(state))
            return default
        return referer

    def _getPas(self):
        pas = api.portal.get_tool('acl_users')
        return pas


class LoginView(BrowserView):
    def _getPas(self):
        pas = api.portal.get_tool('acl_users')
        return pas

    def __call__(self, ):
        """
        """
        pas = self._getPas()
        acl_msal = pas.get('acl_msal')
        request = self.request
        came_from = request.get('came_from', url_for('index'))
        state =  "{}|{}".format(str(uuid.uuid4()), parse.quote(came_from))
        auth_url = acl_msal._build_auth_url(scopes=acl_msal.scope,
                                             state=state)
        return auth_url


