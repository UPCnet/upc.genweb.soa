# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName


class BUS_properties():

    expected_properties = ['bussoa_user', 'bussoa_password']

    def __init__(self, site):
        self.properties = getToolByName(site,
                                'portal_properties').site_properties
        # Crear propietats per defecte si no existeixen
        self._init_properties()

    def _init_properties(self):
        """Creació de les propietats per defecte"""
        properties = self.properties
        for a in self.expected_properties:
            if properties.hasProperty(a) == 0:
                properties.manage_addProperty(a, '', 'string')

    def get_all(self):
        """Retorna un diccionari amb totes les propietats"""
        props = {}
        # __init__ ens asegura que les propietats existeixen
        for a in self.expected_properties:
            props[a] = getattr(self.properties, a)
        return props


class GN6_Properties(BUS_properties):

    def __init__(self, site):

        self.expected_properties.extend([
                            'gn6_user',
                            'gn6_password',
                            'gn6_domain',
                            'wsdl_gestiotiquets'
                        ])
        # Inicialitzem el pare
        BUS_properties.__init__(self, site)


class GuiaDocentPublica_Properties(BUS_properties):

    def __init__(self, site):
        self.expected_properties.extend([
                            'wsdl_guiadocentpublica'
                        ])
        # Inicialitzem el pare
        BUS_properties.__init__(self, site)
