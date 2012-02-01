# -*- coding: utf-8 -*-
from Products.CMFPlone import PloneMessageFactory as _

from upc.genweb.soa.gn6 import GuiaDocentPublica
from upc.genweb.soa.soaBrowserView import SOABrowserView
from upc.genweb.soa.gn6_properties import GuiaDocentPublica_Properties


class ObtenirPDFView(SOABrowserView):

    #__call__ = ViewPageTemplateFile('altaTiquet.pt')

    def __call__(self):
        pdf = self.obtenir_pdf()
        if pdf is not None:
            return pdf
        return

    def obtenir_pdf(self):
        properties = GuiaDocentPublica_Properties(self.context)
        p = properties.get_all()

        # Comprovem que el GW estigui configurat per treballar amb el GN6
        if p['wsdl_guiadocentpublica'] == '':
            self._error(_("No s'ha configurat el servei guia docent"))
            return

        g = GuiaDocentPublica(p['bussoa_user'],
                p['bussoa_password'],
                p['wsdl_guiadocentpublica'])

        # Obtenim els parametres de la petició
        f = self.request.form
        if 'test' in f:
            g.mode_test()

        # Cridem a l'alta al gestor
        t = g.obtenir_pdf(f)

        # Processem el retorn
        missatge = ''
        tipus = 'info'
        pdf = ''
        if g.resultat_ok():
            pdf = t.PDF
            missatge = "Crida correcte"
            self.request.response.setHeader("Content-type", "application/pdf")
            return pdf
        else:
            tipus = 'error'
            missatge = g.ultim_error()
            self.context.plone_utils.addPortalMessage(missatge, tipus)
            self._redirect()
