# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName


class DadesUsuariView(BrowserView):

    template = ViewPageTemplateFile('dadesUsuari.pt')
    params = ['servei', 'subservei', 'codiServei', 'codiSubservei']
    dades = []

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.dades = self.request.form

    def __call__(self):
        #Validació dels parametres d'entrada
        for a in self.params:
            if a not in  self.dades:
                self.context.plone_utils.addPortalMessage(
                "Falten dades, contacta amb el gestor del genweb", 'error')
                self.request.response.redirect(self.get_redirect_url())
                return
        return self.template()

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
