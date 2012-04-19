# -*- coding: utf-8 -*-
from upc.genweb.soa import SOAMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView


class NoDisponibleView(BrowserView):

    __call__ = ViewPageTemplateFile('nodisponible.pt')

    def __init__(self, context, request):
        self.request = request
        self.context = context

    def message(self):
        params = self.request.form
        dataInici = None
        dataFi = None
        if 'dataInici' in params:
            dataInici = params['dataInici']
            dataInici = self.context.toLocalizedTime(dataInici)
        if 'dataFi' in params:
            dataFi = params['dataFi']
            dataFi = self.context.toLocalizedTime(dataFi)

        if dataInici and dataFi:
            return _("El termini per realitzar sol·licituds per aquesta prestació és del $dataInici al ${dataFi}.",
                mapping={"dataFi": dataFi, "dataInici": dataInici})
        elif dataInici and not dataFi:
            return _("El termini per realitzar sol·licituds per aquesta prestació comença el ${dataInici}.",
                mapping={"dataInici": dataInici})
        elif dataFi:
            return _("El termini per realitzar sol·licituds per aquesta prestació va finalitzar el ${dataFi}.",
                mapping={"dataFi": dataFi})
        return _('No es poden realitzar sol·licituds per aquesta prestació.')
