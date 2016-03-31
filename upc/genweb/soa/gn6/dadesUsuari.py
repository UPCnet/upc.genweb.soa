# -*- coding: utf-8 -*-
from z3c.form import form, field, button, interfaces, util
from upc.genweb.soa.interfaces import IGN6DadesAltaForm
from upc.genweb.soa import SOAMessageFactory as _
from upc.genweb.soa.gn6.altaTiquet import AltaTiquet
from datetime import date


class DadesAltaForm(form.Form, AltaTiquet):

    #Routa de la pàgina de servei no disponible (mirar configure.zml)
    NO_DISPONIBLE = '/gn6-no-disponible'

    fields = field.Fields(IGN6DadesAltaForm)
    # Aquet formulari no té titol (label)
    label = _(u"Creació d'una nova sol·licitud")
    # TODO millora: desar el nom del gestor en una property
    description = _(u"Omple els camps amb la informació de la sol·licitud. A partir d'aquesta és crearà un nou tiquet al gestor e-serveiscbl")

    ignoreContext = True

    def _getDateFromImputOrToday(self, id):
        """ Obte el paremetre id de la petició i el tracta com una data separada
         per '-', tal com la retorna z3c.form. Si no troba el parametre et retornar
         el valor per defecte z3c
         """
        if id in self.request.form:
            dts = self.request.form[id].split('-')
            data = date(int(dts[0]), int(dts[1]), int(dts[2]))
        else:
            data = date.today()
        return data

    def _getUriNoDisponible(self):
        uri = self.context.portal_url() + self.NO_DISPONIBLE
        # Volem filtrar els parametres de la petició i obtenir només les dates
        param_list = ['dataInici', 'dataFi']
        params = []
        for param in param_list:
            if param in self.request.form:
                params.append(param + '=' + self.request.form[param])
        # Unim els parametres de la llista amb &
        params = '&'.join(params)
        # Si hi havia algun parametre els afegim a la uri
        if params != '':
            uri += '?' + params
        return uri

    def updateWidgets(self):
        """ Ocultar camps a l'usuari final
        """
        # L'usuari esta identificat?
        if not self._get_user():
            came_from = self.request.getURL()
            self.request.response.redirect(self.context.portal_url() + '/login?came_from=' + came_from)
            return
        # Validació del periode
        dataInici = self._getDateFromImputOrToday('dataInici')
        dataFi = self._getDateFromImputOrToday('dataFi')
        if dataInici > date.today() or dataFi < date.today():
            # Redirigim a la pàgina no disponible
            self.request.response.redirect(self._getUriNoDisponible())
            return
        form.Form.updateWidgets(self)

        # Amagem alguns camps
        self.widgets['dataInici'].mode = interfaces.HIDDEN_MODE
        self.widgets['dataFi'].mode = interfaces.HIDDEN_MODE
        del self.widgets['dataInici']
        del self.widgets['dataFi']
        link_fields = ['equipResolutor', 'producte', 'subservei']
        for a in link_fields:
            if a in self.request.form:
                self.widgets[a].value = self.request.form[a]
            self.widgets[a].mode = interfaces.HIDDEN_MODE

        self.widgets['redirect'].mode = interfaces.HIDDEN_MODE
        if self.widgets['redirect'].value == '':
            self.widgets['redirect'].value = self._get_redirect()

    @button.buttonAndHandler(_(u"Envia"))
    def envia(self, action):
        data, errors = self.extractData()

        if errors:
            self.status = self.formErrorsMessage
            return

        annexe = None

        # Comprovem si hi ha cap annexe
        if data['annexe'] is not None:
            # Obtenim el nom del fitxer i el contingut
            annexe = {
                'name': util.extractFileName(self, 'form-widgets-annexe'),
                'data': data.pop('annexe')
                }
        # Cridem a l'alta
        result = self.alta(data, annexe)

        # Procesem resultats
        self.status = result['message']
        if result['code'] == self.OK:
            self.context.plone_utils.addPortalMessage(result['message'], 'info')
            self._redirect()
            return ''
