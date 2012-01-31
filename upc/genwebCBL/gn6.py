# -*- coding: utf-8 -*-
from suds.wsse import UsernameToken
from suds.wsse import Security
from suds.client import Client
from Products.CMFPlone import PloneMessageFactory as _


class BUS_Errors():

    DEFAULT = 'default'
    # CUSTOM errors
    BAD_REQUEST = 400
    FORBIDEN = 403
    TEST_OK = 'test_ok'

    _descripcions = {
        BAD_REQUEST:
        _('La crida al Gestor de Serveis no es correcte'),
        TEST_OK: _("TEST: finalitzat correctament"),
        DEFAULT:
        _('Hi ha hagut un problema inesperat amb la petició al Gestor')
    }

    def getDescription(self, code):
        # Busquem la descripcio
        if code in self._descripcions:
            return self._descripcions[code]
        # No coneixem el codi d'error
        else:
            return self._descripcions[self.DEFAULT]


class GN6_Errors(BUS_Errors):

    # GN6 errors
    USER_NOT_FOUND = "-2"
    WRONG_PERMISSION = "-3"

    def __init__(self):
        self._descripcions.update({
            # El sol·licitant no existeix
            self.USER_NOT_FOUND:
            _("No s'ha trobat el teu usuari al Gestor de Serveis."),
            # El sol·licitant no té rol de sol·licitant de tiquets en el domini
            self.WRONG_PERMISSION:
            _("No tens permissos per crear tiquets al Gestor de Serveis.")
            })


class GuiaDocentPublica_Errors(BUS_Errors):

    ERROR = "-1"

    def __init__(self):
        self._descripcions.update({
            self.ERROR:
            _("Hi ha hagut un error")
            })


class Bus_SOA_Client():

    last_result = None
    last_error = None
    test = False
    CODE_OK = "1"

    def __init__(self, bus_user, bus_pass, wsdl):
        # Crear client SOA amb Securitiy activat
        self.client = Client(wsdl)
        security = Security()
        token = UsernameToken(bus_user, bus_pass)
        security.tokens.append(token)
        self.client.set_options(wsse=security)

    def mode_test(self):
        """Activa el mode test, no es fan les peticions al servei SOA,
         només es validen"""
        self.test = True


class GuiaDocentPublica(Bus_SOA_Client):

    def __init__(self, bus_user, bus_pass, wsdl):
        Bus_SOA_Client.__init__(self, bus_user, bus_pass, wsdl)
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

        if data['codi'] != '':
            data['codi'] = int(data['codi'])

        if not self.test:
            try:
                self.last_result = self.client.service.obtenirPDF(data['codi'], data['curs'], data['grup'], data['idioma'])
            except:
                pass
        else:
            self.last_error = self.errors.TEST_OK

        return self.last_result


class GN6_GestioTiquets(Bus_SOA_Client):

    SERVEI = 'https://bus-soades.upc.edu/gN6/GestioTiquetsv1?wsdl'

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

    def __init__(self, gn6_user, gn6_pass, gn6_domain, bus_user, bus_pass):
        """Inciialització del client"""
        # Desar variables per fer servir més tard
        self.usuari = gn6_user
        self.password = gn6_pass
        self.domain = gn6_domain
        # Crear client SOA amb Securitiy activat
        self.client = Client(self.SERVEI)
        security = Security()
        token = UsernameToken(bus_user, bus_pass)
        security.tokens.append(token)
        self.client.set_options(wsse=security)
        # Gestor d'errors
        self.errors = GN6_Errors()

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

    def alta_tiquet(self, params):
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
            if a in params and params[a] != '':
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
        data['ip'] = ''
        # Crida al servei SOA
        if not self.test:
            self.last_result = self.client.service.AltaTiquet(**data)
            print self.client.last_sent().plain()
        else:
            self.last_error = self.errors.TEST_OK

        return self.last_result

    def alta_params(self):
        return ['solicitant', 'assumpte', 'descripcio', 'equipResolutor',
                'assignatA', 'producte',    'urgencia', 'impacte', 'proces',
                 'procesOrigen', 'estat', 'ip', 'enviarMissatgeCreacio',
                 'enviarMissatgeTancament', 'infraestructura']
