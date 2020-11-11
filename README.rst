.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://travis-ci.org/collective/collective.msal.svg?branch=master
    :target: https://travis-ci.org/collective/collective.msal

.. image:: https://coveralls.io/repos/github/collective/collective.msal/badge.svg?branch=master
    :target: https://coveralls.io/github/collective/collective.msal?branch=master
    :alt: Coveralls

.. image:: https://img.shields.io/pypi/v/collective.msal.svg
    :target: https://pypi.python.org/pypi/collective.msal/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/collective.msal.svg
    :target: https://pypi.python.org/pypi/collective.msal
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/collective.msal.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/collective.msal.svg
    :target: https://pypi.python.org/pypi/collective.msal/
    :alt: License


===============
collective.msal
===============


Features
--------

Simple PAS plugin that allows to a Microsoft Tenant users to authenticate on Plone. It relies on:
 - Microsoft Authentication Library (MSAL Python library)
 - plone.session (PAS plugin)

Documentation
-------------

The authentication happens on the Microsoft server side and then, if succeeded,
it creates a local plone.session token keeping the plone user authenticated.

User documentation (in short)
#############################

1. Setup an Azure App on Microsoft Azure Portal
2. Configure environment vars in buildout configuration/ZMI
3. Install the product collective.msal in plone control panel
4. Use the [sign in with microsoft] button, that has been added to the login form, to authenticate
5. enjoy

User documentation (little bit longer)
######################################

You have to setup your APP separately on Microsoft Azure portal first; then locally.

In the Azure Microsoft Platform:
********************************

1. Register your application. This will provides you the CLIENT_ID and directory id of the tenant you will use as AUTHORITY parameter
2. Configure your application in order to generate a CLIENT_SECRET
3. Define a REDIRECT_PATH (by default: /collective.msal.getAToken). You can set these parameters as enviroment variabiles in buildout configuration  (see `Installation`_)
4. Setup other Azure stuff according to Microsoft Documentation

Locally:
********

5. In the instance buildout section: set environment variables properly. see `Installation`_
6. In Plone: Install the product via plone control panel. This will adds a Plone/acl_users/acl_msal plugin and overrides (z3c.jbot) the login form adding the Microsoft sign in button
7. In ZMI Plone -> acl_users -> acl_msal -> Properties TAB: Verify the parameters CLIENT_ID, CLIENT_SECRET, AUTHORITY, and REDIRECT_PATH (this one by default should point to /collective.msal.getAToken)

If you want to write down your login form you may want to use the followig helper to generate the login href::

     Plone/@@collective.msal.login
  
 
Translations
------------

This product has been translated into

 - not really needed so far
 

Installation
------------

Install collective.msal by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.msal

    [instance]
    
    ...
    
    enviroment-vars +=
        CLIENT_ID 25305d7c-xxxx-yyyy-zzzz-abcdefg998877
        CLIENT_SECRET secret
        AUTHORITY https://login.microsoftonline.com/<ID_DIRECTORY_TENANT>
        REDIRECT_PATH /collective.msal.getAToken
    

and then running ``bin/buildout -Nv``


Contribute
----------

.. - Issue Tracker: https://github.com/collective/collective.msal/issues
- Issue Tracker: https://github.com/sauzher/collective.msal/issues
.. - Source Code: https://github.com/collective/collective.msal
- Source Code: https://github.com/sauzher/collective.msal
.. - Documentation: https://docs.plone.org/foo/bar

Support
-------

If you are having issues, please let me know opening an issue here https://github.com/sauzher/collective.msal/issues


License
-------

The project is licensed under the GPLv2.
