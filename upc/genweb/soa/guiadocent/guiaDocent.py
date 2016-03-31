# -*- coding: utf-8 -*-
from Products.CMFPlone import PloneMessageFactory as _
from upc.genweb.soa.bus import BUS_Errors, BUS_properties, Bus_SOA_Client
from upc.genweb.soa.soaBrowserView import SOABrowserView
import logging


class GuiaDocentPublica_Properties(BUS_properties):

    def __init__(self, site):
        self.expected_properties.extend(['wsdl_guiadocentpublica'])
        # Inicialitzem el pare
        BUS_properties.__init__(self, site)


class GuiaDocentPublica_Errors(BUS_Errors):

    ERROR = "-1"

    def __init__(self):
        self._descripcions.update({
            self.ERROR: _(u"Hi ha hagut un error")
            })


class GuiaDocentPublica(Bus_SOA_Client):

    def __init__(self, bus_user, bus_pass, wsdl):
        Bus_SOA_Client.__init__(self, bus_user, bus_pass, wsdl)
        self.errors = GuiaDocentPublica_Errors()
        self.CODE_OK = 0

    def obtenir_pdf_params(self):
        return ['codi', 'curs', 'grup', 'idioma']

    def resultat_ok(self):
        """Retorna si la darrera petició ha acabat correctament"""
        return self.last_result != None and self.last_result.error == self.CODE_OK

    def ultim_error(self):
        # Comprobem la darrera petició si s'ha cridad correctament
        if self.last_result is not None:
            if self.last_result.error != self.CODE_OK:
                return self.last_result.missatge
        # Comprobem si la darrera petició no s'ha arribat a cridar
        elif self.last_error is not None:
            return self.errors.getDescription(self.last_error)
        return None

    def obtenir_pdf(self, params):
        self.last_result = None
        self.last_error = None

        check = self.obtenir_pdf_params()
        data = {}
        obligatoris = {}
        # Recuperem els valors per la petició del diccionari que rebem com
        #  parametre
        for a in check:
            if a in params and params[a] != '':
                data[a] = params[a]
            # Alguns paramtres son obligatoris
            elif a in obligatoris:
                #TODO logger?
                self.last_error = self.errors.BAD_REQUEST
                return None
            else:
                data[a] = ''
        # Comentem aquesta linia ja que el parametre codi, a vegades inclou lletres... (ex: 820011A)
        #if data['codi'] != '':
        #    data['codi'] = int(data['codi'])

        if not self.test:
            try:
                self.last_result = self.client.service.obtenirPDF(data['codi'], data['curs'], data['grup'], data['idioma'])
            except Exception, excepcio:
                self.last_error = self.errors.DEFAULT
                logger = logging.getLogger('SOA')
                logger.exception(excepcio)
        else:
            self.last_error = self.errors.TEST_OK

        return self.last_result


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
            self._error(_(u"No s'ha configurat el servei guia docent"))
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
            missatge = _(u"Crida correcte")
            self.request.response.setHeader("Content-type", "application/pdf")
            return pdf
        else:
            tipus = 'error'
            missatge = g.ultim_error()
            self.context.plone_utils.addPortalMessage(missatge, tipus)
            self._redirect()
