# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from z3c.form import form, field, button
from upc.genweb.soa.interfaces import IGN6UrlHelperForm
from upc.genweb.soa import SOAMessageFactory as _
from upc.genweb.soa.soaBrowserView import  SOABrowserView


class HelperAltaForm(form.Form, SOABrowserView):

    fields = field.Fields(IGN6UrlHelperForm)
    label = _(u"Nou enllaç d'alta de tiquet al GN6")
    description = _(u"Utilitza els camps per generar un nou enllaç que permeti crear un tiquet predefint al gestor de serveis.")

    ignoreContext = True

    def updateWidgets(self):
        # Comprovem que l'usuari té permisos d'edició a la carpeta arrel
        form.Form.updateWidgets(self)
        if not self.havePermissionAtRoot():
            self._error(_('No tens permissos per accedir aquest recurs'))
            self._redirect()

    @button.buttonAndHandler(_(u"Crea l'enllaç"))
    def creaLink(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        params = ''
        sep = ''
        for key in data:
            if data[key] is not None:
                params += sep + key + "=" + data[key]
            sep = '&'

        desti = 'gn6-helper-alta-view?' + params
        self.request.response.redirect(desti)


class HelperAltaView(SOABrowserView):

    def __call__(self):
        # Comprovem que l'usuari té permisos d'edició a la carpeta arrel
        vista = ViewPageTemplateFile('helper.pt')
        if self.havePermissionAtRoot():
            return vista()
        self._redirect()
        return

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def get_url(self):
        return self.request["QUERY_STRING"]
