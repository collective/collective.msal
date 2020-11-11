===============
collective.msal
===============

Simple PAS plugin that relies on two pieces of software:
 - Microsoft Authentication Library (MSAL Python library)
 - plone.session (PAS plugin)

The authentication happens on the Microsoft server side and then, if succeded,
it creates a local plone.session token keeping the plone user authenticated.

User documentation (short)
   0. Setup an Azure App on Microsoft Azure Portal
   1. Configure environment vars in buildout configuration
   2. Install the product collective.msal in plone control panel
   3. Use the [sign in with microsoft] button that will be added to the login form
   4. enjoy


User documentation (little bit longer)

In order to make things to work you have to.

In the Azure Microsoft Platform:
    a. Register your application in the Azure Microsoft Platform.
    This will provides you the CLIENT_ID and directory id of the tenant you will use as AUTHORITY parameter

    b. In the Azure Microsoft portal: configure your application in order to generate a CLIENT_SECRET

    c. In the Azure Microsoft portal: define a REDIRECT_PATH (by default: /collective.msal.getAToken)
    You can set these parameters as enviroment variabiles in buildout configuration  (see below)

    d. In the Azure Microsoft portal:setup other Azure stuff according to Microsoft Documentation

Locally:
    a. In the instance buildout section: set environment variables properly

[instance]
...

environment-vars +=
   CLIENT_ID 25305d7c-xxxx-yyyy-zzzz-abcdefg998877
   CLIENT_SECRET secret
   AUTHORITY https://login.microsoftonline.com/<ID_DIRECTORY_TENANT>
   REDIRECT_PATH /collective.msal.getAToken


   b. In Plone: Install the product via plone control panel
    This will add a Plone/acl_users/acl_msal, and override the login form adding to it the Microsoft sign in button
   c. In ZMI Plone -> acl_users -> acl_msal -> Properties TAB: Verify the parameters CLIENT_ID, CLIENT_SECRET, AUTHORITY, and REDIRECT_PATH
    (this one by default should point to /collective.msal.getAToken)

