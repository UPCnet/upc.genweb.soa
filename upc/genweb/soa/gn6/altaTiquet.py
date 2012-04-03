# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

from upc.genweb.soa.gn6.gn6 import GN6_GestioTiquets, GN6_Properties


class AltaTiquet():

    ERROR = -1
    OK = 1

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

    def _get_redirect(self):
        redirect = self.request.get('HTTP_REFERER')
        if redirect is None or redirect == '':
            redirect = self._get_portal_url()
        return redirect

    def _redirect(self):
        """ Redirecciona a la pàgina d'on venia l'usuari, o la pàgina anterior
        al formulari o a la pàgina principal si el camp HTTP_REFERER"""
        #TODO provar
        if 'redirect' in self.request.form:
            redirect = self.request.form['redirect']
        else:
            redirect = self._get_redirect()
        # Redirecció
        self.request.response.redirect(redirect)

    def _error(self, missatge):
        """Acaba la petició redireccionant i mostrant un missatge d'error"""
        self.context.plone_utils.addPortalMessage(missatge, 'error')
        self._redirect()
        #TODO exit?

    def _status(self, missatge, code):
        return {'message': missatge, 'code': code}

    #TODO potser seria millor cridar a l'alta a l'init
    # i amb aquest metode només obtenir el resultat
    def alta(self, params, annexe):
        gn6_prop = GN6_Properties(self.context)
        p = gn6_prop.get_all()
        # Obtenim l'usuari i comprovem l'usuari
        user = self._get_user()
        if user is None:
            return self._status(_('Permissos insuficients'), self.ERROR)

        # Comprovem que el GW estigui configurat per treballar amb el GN6
        if p['gn6_user'] == '':
            return self._status(_("No s'ha configurat el Gestor de Serveis",
                    self.ERROR))

        g = GN6_GestioTiquets(
            p['gn6_user'], p['gn6_password'], p['gn6_domain'],
            p['bussoa_user'], p['bussoa_password'], p['wsdl_gestiotiquets']
            )

        # Obtenim els parametres de la petició
        if 'test' in params:
            g.mode_test()
        # Hi han parametres no modificables amb el formulari,
        # els esborrem de la crida
        desactivats = ['estat', 'ip', 'solicitant', 'client']
        for a in desactivats:
            if a in params:
                del params[a]

        #TODO Sanitize?

        # Camps que fixats
        #TODO Potser seria millor self.request.getClientAddr()?
        params['ip'] = self._get_ip()
        params['solicitant'] = user.getId()

        # Cridem a l'alta al gestor
        t = g.alta_tiquet(params, annexe)

        # Processem el retorn
        if g.resultat_ok():
            missatge = _("S'ha creat un tiquet amb identificador ${codi}",
             mapping={'codi': t.codiTiquet})
            return self._status(missatge, self.OK)
        else:
            missatge = g.ultim_error()
            return self._status(missatge, self.ERROR)


class AltaTiquetView(AltaTiquet, BrowserView):

    __call__ = ViewPageTemplateFile('altaTiquet.pt')

    def __init__(self, context, request):
        self.request = request
        self.context = context

    def alta(self):
        result = AltaTiquet.alta(self, self.request.form)
        if result['code'] == 1:
            self.context.plone_utils.addPortalMessage(result['message'],
                    'info')
            self._redirect()
        else:
            self._error(result['message'])
