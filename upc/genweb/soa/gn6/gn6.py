# -*- coding: utf-8 -*-
from Products.CMFPlone import PloneMessageFactory as _
from upc.genweb.soa.bus import BUS_Errors, BUS_properties, Bus_SOA_Client
import logging
from base64 import b64encode

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


class GN6_Errors(BUS_Errors):

    # GN6 errors
    USER_NOT_FOUND = "-2"
    WRONG_PERMISSION = "-3"
    WRONG_PERMISSION_2 = "-9"
    SUBSERVEI_NOT_FOUND = "-11"

    def __init__(self):
        self._descripcions.update({
            # El sol·licitant no existeix
            self.USER_NOT_FOUND:
                _("No s'ha trobat el teu usuari al Gestor de Serveis."),
            # El sol·licitant no té rol de sol·licitant de tiquets en el domini
            self.WRONG_PERMISSION:
                _("No tens permissos per crear tiquets al Gestor de Serveis."),
            self.WRONG_PERMISSION_2:
                _("No tens permissos per crear tiquets al Gestor de Serveis."),
            self.SUBSERVEI_NOT_FOUND:
                _("No s'ha trobat el subservei pel servei sol·licitat."),
            })


class GN6_GestioTiquets(Bus_SOA_Client):

    # Diccionaris amb valors posibles
    # Gravetat del tiquet
    _dic_gravetats = {'baixa': 'GRAVETAT_BAIXA',
                        'mitja': 'GRAVETAT_MITJA',
                        'alta': 'GRAVETAT_ALTA'}
    # Proces i proces origen
    _dic_processos = {'aus': 'PROCES_AUS',
                        'rin': 'PROCES_RIN',
                        'pti': 'PROCES_PTI',
                        'ads': 'PROCES_ADS',
                        'adm': 'PROCES_ADM',
                        'dso': 'PROCES_DSO',
                        'fcl': 'PROCES_FCL',
                        'aid': 'PROCES_AID',
                        'apv': 'PROCES_APV'}

    _dic_processos_origen = {'aus': 'PROCES_AUS',
                        'ads': 'PROCES_ADS',
                        'aid': 'PROCES_AID',
                        'apv': 'PROCES_APV'
                        }
    # Estat
    _dic_estats = {'obert': 'TIQUET_STATUS_OBERT',
                    'pendent': 'TIQUET_STATUS_PEND',
                    'tancat': 'TIQUET_STATUS_TANCAT'}
    # Impacte
    _dic_impacte = {'baix': 'II_BAIX', 'alt': 'II_ALT'}

    # Si/no: transformació dels valors sí/no als valors del servei SOA
    _dic_sino = {'sí': 'S', 'si': 'S', 's': 'S', 'n': 'N', 'no': 'N'}

    def _dic_translate(self, key, dic):
        if key in dic:
            return dic[key.lower()]
        return None

    def __init__(self, gn6_user, gn6_pass, gn6_domain, bus_user, bus_pass, wsdl):
        """Inciialització del client"""
        Bus_SOA_Client.__init__(self, bus_user, bus_pass, wsdl)
        # Gestor d'errors
        self.errors = GN6_Errors()
        # Desar variables per fer servir més tard
        self.usuari = gn6_user
        self.password = gn6_pass
        self.domain = gn6_domain

        self.diccionaris = {'proces': self._dic_processos,
                            'procesOrigen': self._dic_processos_origen,
                            'urgencia': self._dic_gravetats,
                            'impacte': self._dic_impacte,
                            'enviarMissatgeCreacio': self._dic_sino,
                            'enviarMissatgeTancament': self._dic_sino}

    def resultat_ok(self):
        """Retorna si la darrera petició ha acabat correctament"""
        return self.last_result != None and self.last_result.codiRetorn == self.CODE_OK

    def ultim_error(self):
        # Comprobem la darrera petició si s'ha cridad correctament
        if self.last_result is not None:
            if self.last_result.codiRetorn != self.CODE_OK:
                return self.errors.getDescription(self.last_result.codiRetorn)
        # Comprobem si la darrera petició no s'ha arribat a cridar
        elif self.last_error is not None:
            return self.errors.getDescription(self.last_error)
        return None

    def alta_tiquet(self, params, annexe):
        """Crea un tiquet al gestor"""
        self.last_result = None
        self.last_error = None
        # Obtenim els parametres de la petició
        check = self.alta_params()

        # Definim els parametres obligatoris
        obligatoris = ['solicitant', 'assumpte']
        data = {}

        # Traduir els valors d'entrada als valors que espera el servei SOA,
        # per exemple baixa -> GRAVETAT_BAIXA
        for i in params:
            if i in self.diccionaris:
                param = params[i]
                if param is not None and param != '':
                    param = param.lower()
                    if param not in self.diccionaris[i]:
                        #TODO logger?
                        self.last_error = self.errors.BAD_REQUEST
                        return None
                    else:
                        trans = self.diccionaris[i][param]
                    params[i] = trans

        # Recuperem els valors per la petició del diccionari que rebem com
        #  parametre
        for a in check:
            if a in params and params[a] is not None:
                data[a] = params[a]
            # Alguns paramtres son obligatoris
            elif a in obligatoris:
                #TODO logger?
                self.last_error = self.errors.BAD_REQUEST
                return None
            else:
                data[a] = ''
        # GN6 security
        data['username'] = self.usuari
        data['password'] = self.password
        data['domini'] = self.domain
        #TODO fixar l'identificador del client
        data['client'] = ''
        # Crida al servei SOA
        if not self.test:
            try:
                self.last_result = self.client.service.AltaTiquet(**data)
                # si te annexe -> cridar al webservice i afegir
                if annexe is not None and self.last_result.codiRetorn == self.CODE_OK:
                    # Preparem les dades de l'annexe
                    dataAnnexe = {'username': self.usuari,
                        'password': self.password,
                        'domini': self.domain,
                        'codiTiquet': self.last_result.codiTiquet,
                        'usuari': data['solicitant'],
                        'nomFitxer': annexe['name'],
                        'fitxerBase64': b64encode(annexe['data'])
                    }
                    result_annexe = self.client.service.AnnexarFitxerTiquet(**dataAnnexe)
                    # Comprobem si s'ha afegit l'annexe
                    if result_annexe.codiRetorn != self.CODE_OK:
                        # Modifiquem la descripció del darrer resultat
                        self.last_result.descripcioError = _("S'ha creat el tiquet, però no s'ha pogut afegir l'annexe.")

            except Exception, excepcio:
                self.last_error = self.errors.DEFAULT
                logger = logging.getLogger('SOA')
                logger.exception(excepcio)
            #print self.client.last_sent().plain()
        else:
            self.last_error = self.errors.TEST_OK

        return self.last_result

    def alta_params(self):
        return ['solicitant', 'assumpte', 'descripcio', 'equipResolutor',
                'assignatA', 'producte',    'urgencia', 'impacte', 'proces',
                 'procesOrigen', 'estat', 'ip', 'enviarMissatgeCreacio',
                 'enviarMissatgeTancament', 'infraestructura', 'subservei']
