# -*- coding: utf-8 -*-
from z3c.form import form, field, button, interfaces, util
from upc.genweb.soa.interfaces import IGN6DadesAltaForm
from upc.genweb.soa import SOAMessageFactory as _
from upc.genweb.soa.gn6.altaTiquet import AltaTiquet
from datetime import date


class DadesAltaForm(form.Form, AltaTiquet):

    fields = field.Fields(IGN6DadesAltaForm)
    # Aquet formulari no té titol (label)
    label = _(u"Creació d'un nou tiquet")
    description = _(u"Omple els camps amb la informació del tiquet.")

    ignoreContext = True

    def updateWidgets(self):
        """ Ocultar camps a l'usuari final
        """
        # L'usuari esta identificat?
        if not self._get_user():
            came_from = self.request.getURL()
            self.request.response.redirect(self.context.portal_url() + '/login?came_from=' + came_from)
            return
        # Validació del periode
        if 'dataInici' in self.request.form:
            dts = self.request.form['dataInici'].split('-')
            dataInici = date(int(dts[0]), int(dts[1]), int(dts[2]))
            if dataInici > date.today():
                self.request.response.redirect(self.context.portal_url() + '/gn6-no-disponible')
                return
        if 'dataFi' in self.request.form:
            dts = self.request.form['dataFi'].split('-')
            dataFi = date(int(dts[0]), int(dts[1]), int(dts[2]))
            if dataFi < date.today():
                self.request.response.redirect(self.context.portal_url() + '/gn6-no-disponible')
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
            self.context.plone_utils.addPortalMessage(result['message'],
                'info')
            self._redirect()
            return ''
