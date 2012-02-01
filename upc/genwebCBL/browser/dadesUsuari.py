# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName


class DadesUsuari():
    params = ['servei', 'subservei', 'codiServei', 'codiSubservei']


class DadesUsuariView(BrowserView):

    params = []
    dades = []

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.params = DadesUsuari().params
        self.dades = self.request.form

    def __call__(self):
        #Validació dels parametres d'entrada
        for a in self.params:
            if a not in  self.dades:
                self.context.plone_utils.addPortalMessage(
                "Falten dades, contacta amb el gestor del web", 'error')
                self.request.response.redirect(self.get_redirect_url())
                return
        template = ViewPageTemplateFile('dadesUsuari.pt')
        return template(self)

    def _get_portal_url(self):
        """ Retorna l'adreça del portal """
        urltool = getToolByName(self.context, 'portal_url')
        portal = urltool.getPortalObject()
        return portal.absolute_url()

    def get_redirect_url(self):
        """ Retorna la pàgina d'on venia l'usuari o a la pàgina
         principal si el camp HTTP_REFERER no està definit"""
        redirect = self.request.get('HTTP_REFERER')
        if redirect is None or redirect == '':
            redirect = self._get_portal_url()
        return redirect

    def get_servei(self):
        return self.dades['servei']

    def get_subservei(self):
        return self.dades['subservei']

    def get_codi_servei(self):
        return self.dades['codiServei']

    def get_codi_subservei(self):
        return self.dades['codiSubservei']


class HelperView(BrowserView):

    __call__ = ViewPageTemplateFile('dadesHelper.pt')
    params = []

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.params = DadesUsuari().params
        self.prettyNames = {'servei': 'Servei',
                            'subservei': 'Subservei',
                            'codiServei': 'Codi subservei',
                            'codiSubservei': 'Codi Servei'
                            }
        self.dades = self.request.form

    def has_data(self):
        for a in self.params:
            if a not in self.dades:
                return False
        return True

    def get_params(self):
        return self.params

    def get_data(self):
        return self.dades

    def get_pretty(self, key):
        return self.prettyNames[key]

    def get_url(self):
        ## Les linies comentades obtenen la url actual i fan un canvi...
        # self.request["ACTUAL_URL"].replace('gn6-helper-url-recollir',
        # 'gn6-recollir-dades')
        return "gn6-recollir-dades?" + self.request["QUERY_STRING"]
