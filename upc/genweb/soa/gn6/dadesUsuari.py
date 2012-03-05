# -*- coding: utf-8 -*-
from z3c.form import form, field, button, interfaces
from upc.genweb.soa.interfaces import IGN6DadesAltaForm
from upc.genweb.soa import SOAMessageFactory as _
from upc.genweb.soa.gn6.altaTiquet import AltaTiquet


class DadesAltaForm(form.Form, AltaTiquet):

    fields = field.Fields(IGN6DadesAltaForm)
    # Aquet formulari no té titol (label)
    label = _(u"Creació d'un nou tiquet")
    description = _(u"Omple els camps amb la informació del tiquet.")

    ignoreContext = True

    def updateWidgets(self):
        """ Make sure that return URL is not visible to the user.
        """
        if not self._get_user():
            came_from = self.request.getURL()
            self.request.response.redirect(self.context.portal_url() + '/login?came_from=' + came_from)
            return
        form.Form.updateWidgets(self)

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
        result = self.alta(data)
        self.status = result['message']
        if result['code'] == self.OK:
            #TODO a on redireccionem?
            self.context.plone_utils.addPortalMessage(result['message'],
                'info')
            self._redirect()
            return ''
