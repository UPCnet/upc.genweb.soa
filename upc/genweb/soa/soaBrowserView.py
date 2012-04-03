# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from AccessControl import getSecurityManager


class SOABrowserView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def _get_user(self):
        """Retorna l'usuari quue esta autenticat al portal"""
        mt = getToolByName(self.context, 'portal_membership')
        if mt.isAnonymousUser():
            #  the user has not logged in
            return None
        else:
            return mt.getAuthenticatedMember()

    def _get_ip(self):
        """ Extract the client IP address from the HTTP request
         in a proxy-compatible way.
        @return: IP address as a string or None if not available"""
        if "HTTP_X_FORWARDED_FOR" in self.request.environ:
            # Virtual host
            ip = self.request.environ["HTTP_X_FORWARDED_FOR"]
        elif "HTTP_HOST" in self.request.environ:
            # Non-virtualhost
            ip = self.request.environ["REMOTE_ADDR"]
        else:
            # Unit test code?
            ip = None
        return ip

    def _get_portal_url(self):
        """ Retorna l'adreça del portal """
        urltool = getToolByName(self.context, 'portal_url')
        portal = urltool.getPortalObject()
        return portal.absolute_url()

    def _redirect(self):
        """ Redirecciona a la pàgina d'on venia l'usuari, o la pàgina anterior
        al formulari o a la pàgina principal si el camp HTTP_REFERER"""
        if 'redirect' in self.request.form:
            redirect = self.request.form['redirect']
        else:
            redirect = self.request.get('HTTP_REFERER')
            if redirect is None or redirect == '':
                redirect = self._get_portal_url()
        # Redirecció
        self.request.response.redirect(redirect)

    def _error(self, missatge):
        """Acaba la petició redireccionant i mostrant un missatge d'error"""
        self.context.plone_utils.addPortalMessage(missatge, 'error')
        self._redirect()
        #TODO exit?

    def havePermissionAtRoot(self):
        """Funcio que retorna si es Editor a l'arrel"""

        pm = getToolByName(self, 'portal_membership')
        tools = getMultiAdapter((self.context, self.request),
                                    name=u'plone_tools')
        proot = tools.url().getPortalObject()
        sm = getSecurityManager()
        user = pm.getAuthenticatedMember()

        return sm.checkPermission('Modify portal content', proot) or ('WebMaster' in user.getRoles())
