# -*- coding: utf-8 -*-
from suds.wsse import UsernameToken
from suds.wsse import Security
from z3c.suds import get_suds_client
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName


class BUS_Errors():

    DEFAULT = 'default'
    # CUSTOM errors
    BAD_REQUEST = 400
    FORBIDEN = 403
    TEST_OK = 'test_ok'

    _descripcions = {
        BAD_REQUEST:
        _('La crida al servei no es correcte.'),
        TEST_OK: _("TEST: finalitzat correctament"),
        DEFAULT:
        _(u'Hi ha hagut un problema amb la petició')
    }

    def getDescription(self, code, extra=None):
        # Busquem la descripcio
        if code in self._descripcions:
            return self._descripcions[code]
        # No coneixem el codi d'error
        else:
            if not extra:
                extra = ''
            else:
                extra = ": " + extra + ' (' + code + ')'
            return self._descripcions[self.DEFAULT] + extra


class BUS_properties():

    expected_properties = ['bussoa_user', 'bussoa_password']

    def __init__(self, site):
        self.properties = getToolByName(site,
                                'portal_properties').soa_properties
        ## Crear propietats per defecte si no existeixen
        #self._init_properties()

    def _init_properties(self):
        """Creació de les propietats per defecte:"""
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


class Bus_SOA_Client():

    last_result = None
    last_error = None
    test = False
    CODE_OK = "1"

    def __init__(self, bus_user, bus_pass, wsdl):
        # Crear client SOA amb Securitiy activat
        # Obtenim el client amb z3c.suds i no amb suds.Client
        self.client = get_suds_client(wsdl)
        security = Security()
        token = UsernameToken(bus_user, bus_pass)
        security.tokens.append(token)
        self.client.set_options(wsse=security)

    def mode_test(self):
        """Activa el mode test, no es fan les peticions al servei SOA,
         només es validen"""
        self.test = True
