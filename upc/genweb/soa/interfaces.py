# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope import schema
from upc.genweb.soa import SOAMessageFactory as _


class ISOALayer(Interface):
    """A layer specific for upc.genweb.soa.

    We will use this to register browser pages that should only be used
    when upc.genweb.core is installed in the site.
    """


class IGN6UrlHelperForm(Interface):
    """Define the fields for the link builder form"""

    equipResolutor = schema.TextLine(
                title=_(u"Equip resolutor"),
                description=_(u"Equip encarregat de resoldre el tiquet"),
                required=False
                )
    producte = schema.TextLine(
                title=_(u"Codi del producte/servei"),
                description=_(u"Identificador del producte/servei al gestor"),
                required=False
                )
    subservei = schema.TextLine(
                title=_(u"Codi del subservei"),
                description=_(u"Identificador del subservei al gestor"),
                required=False
                )
    dataInici = schema.Date(
                title=_(u"Data d'inici"),
                description=_(u"Data en la que es podrà comenaçar a solicitar el servei"),
                required=False
                )
    dataFi = schema.Date(
                title=_(u"Data fi"),
                description=_(u"Data del darrer dia que es podrà solicitar el servei"),
                required=False
                )


class IGN6DadesAltaForm(IGN6UrlHelperForm):
    """Define the fields where the user inputs the contents for a new tiquet"""

    assumpte = schema.TextLine(
                title=_(u"Assumpte"),
                description=_(u"Descripció curta de la raó del tiquet"),
                )
    descripcio = schema.Text(
                title=_(u"Descripció"),
                description=_(u"Descripció detallada de la raó del tiquet")
                )

    annexe = schema.Bytes(
                title=_(u'Annexe'),
                description=_(u"Fitxer que s'afegirà com annexe al tiquet"),
                required=False
                )

    redirect = schema.Text(
                title=_(u"Redirect"),
                description=_(u"Url a la que es retornarà en cas d'èxit")
                )
