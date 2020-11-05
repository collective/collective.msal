# -*- coding: utf-8 -*-
from logging import getLogger
from zope.i18nmessageid import MessageFactory

PROJECT_NAME = 'collective.msal'

logger = getLogger(PROJECT_NAME)
_ = MessageFactory(PROJECT_NAME)

