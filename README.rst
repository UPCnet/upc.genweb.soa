UPC.Genweb.SOA
==============

Aquest paquet ofereix la integracio de diferents dels serveis SOA de la UPC per al Genweb.

Actualment suporta la creacio de tiquets al gestor de serveis i la consulta de guies docents publiques.

L'activacio de cadascun dels serveis es fa sota demanda.

.. contents:: Continguts





Configuracio
------------

Quan s'instal·la el paquet per primer cop crea un full de propietats buit **soa_properties** que s'ha d'omplir per poder connectar-se al `bus SOA` i els diferents serveis, els parametres d'aquesta configuracio basics son:

:bussoa_user: usuari del bus SOA.
:bussoa_password: contrasenya de l'usuari del bus SOA.

.. note::

    L'*usuari del bus SOA* s'ha de demanar al **Govern SOA** i ha d'autoritzar les maquines que s'hi connectin.

Gestor de serveis
+++++++++++++++++
:gn6_user: usuari del Gestor de serveis.
:gn6_password: contrasenya de l'usuari del Gestor de serveis.
:gn6_domain: domini del Gestor de serveis.
:wsdl_gestiotiquets: url al fitxer wsdl del gestor de tiquets.

.. note::

    L'*usuari del gestor de serveis* s'ha de demanar a la persona que gestiona el **Gestor de serveis**.

Guia docent publica
+++++++++++++++++++
:wsdl_guiadocent: url al fitxer wsdl de la guia docent publica.

Gestor de serveis
-----------------

La integracio amb el Gestor de serveis integra la creacio de tiquets des de el Genweb preomplint alguns camps per automatizar el proces. Per crear els tiquets s'ofereix:

- Una vista per als editors, que facilita el proces de creacio dels enllacos de creacio predefinits i seleccionar el periode en el que es podra crear el tiquet.
- Un formulari per demanar camps a l'usuari abans de crear el tiquet.
- Una vista que crea un tiquet en funcio dels parametres d'entrada.

Les vistes que facilita aquesta paquet son:

- Creacio de l'enllac per demanar informacio del tiquet

Creacio de l'enllac per demanar informacio
++++++++++++++++++++++++++++++++++++++++++

*/gn6-helper-alta-form*

.. warning::

    Aquesta vista nomes esta disponible pels usuaris amb permissos *Pot editar* a la carpeta arrel.

Aquesta vista permet generar enllacos que porten al formulari de creacio de tiquet, es mostra un formulari amb els camps que es poden predefinir:

- Equip resolutor
- Codi del producte o servei
- Codi del subservei

Un cop s'han entrat els camps que es volen predefinir i enviada la peticio es mostrara una pagina amb l'enllac que s'haura de copiar i un exemple.

.. note::

    El enllacos suporten predefinir mes camps de manera manual, consulteu la llista de camps predefinibles per saber mes detalls.

.. TODO: llista de camps


Creacio d'enllacos d'alta tiquet manuals
++++++++++++++++++++++++++++++++++++++++


Per generar els enllacos de creacio de tiquets manualment hi han dues opcions: `<form/>` o `<a/>`; les dues opcions porten al mateix resultat final, pero cadascuna te els seus pros i contres.

**Enllac**

*Pros*

- Facil de crear i personalitzar: ideal si es vol fer que l'enllac sigui una imatge.
- No s'ha de modificar la configuracio per defecte del Genweb.

*Contras*

- Poc administrable si es defineixen molts parametres.


**Formulari**

*Pros*

- Gestio dels parametres mes facil

*Contras*

- Si es vol enviar la informacio al clicar a una imatge cal javascript.
- S'ha de modificar la configuracio per defecte del Genweb.

.. note::

    Les modificacions al Genweb s'han de demanar.


Code snippets
+++++++++++++

Configuracio extra
..................
**Creacio d'enllacos amb formulari i proves**

Per poder afegir els enllacos utilitzant formularis cal permetre les etiquetes `form` i `input` a la configuracio del *Filtratge Html*.

**Proves**

El formulari de proves utilitza les etiquetes `select` i `option` per generar els desplegables.

Enllac
......

Enllac amb assumpte de prova::

    <a href="gn6-alta-tiquet?assumpte=Prova+amb+href">
        <img src="http://seuelectronica.upc.edu/perfil-de-contractant/imatges/imatge-per-a-contacte"/>
    </a>

Formulari
.........

El codi seguent es un formulari que permet fer proves i generar url's valides::

    <form method="get" action="gn6-alta-tiquet" id="servei1form">
        Assumpte <input name="assumpte" type="text" /><br />
        Descripcio <br/><textarea name="descripcio" type="text"><textarea/><br />
        Resolutor <input name="equipResolutor" type="text" /> <br />
        Assignat a<input name="assignatA" type="text" /> <br />
        Producte<input name="producte" type="text" /> <br />
        Urgencia <select name="urgencia
            <option value=""></option>
            <option value="baixa">Baixa</option>
            <option value="mitja">Mitja</option>
            <option value="alta">Alta</option>
        </select><br/>
        Impacte <select name="impacte">
            <option value=""></option>
            <option value="baix">Baix</option>
            <option value="alt">Alt</option>
        </select><br/>
        Proces proces origen <select name="procesOrigen">
            <option value=""></option>
            <option value="aus">AUS</option>
            <option value="ads">ADS</option>
            <option value="aid">AID</option>
            <option value="apv">APV</option>
        </select><br/>
        Proces <select name="proces">
            <option value=""></option>
            <option value="aus">AUS</option>
            <option value="rin">RIN</option>
            <option value="pti">PTI</option>
            <option value="aid">AID</option>
            <option value="ads">ADS</option>
            <option value="aus">FCL</option>
            <option value="aus">APV</option>
        </select><br/>


        Enviar Creacio<input name="enviarMissatgeCreacio" type="text" /> <br />
        Enviar Tancament<input name="enviarMissatgeTancament" type="text" /> <br />
        Infraestructura<input name="infraestructura" type="text" /> <br />


        <!-- boto per enviar -->
        <input type="submit" value="Envia">
    </form>

Formulari amb els camps ocults per a us d'usuari final::

    <form method="get" action="gn6-alta-tiquet" id="servei2form">
        <input name="assumpte" type="hidden" value=""/>
        <input name="descripcio" type="hidden" value=""/>
        <input name="equipResolutor" type="hidden" value=""/>
        <input name="assignatA" type="hidden" value=""/>
        <input name="producte" type="hidden" value=""/>
        <input name="urgencia" type="hidden" value=""/>
        <input name="impacte" type="hidden" value=""/>
        <input name="proces" type="hidden" value=""/>
        <input name="procesOrigen" type="hidden" value=""/>
        <input name="enviarMissatgeCreacio" type="hidden" value=""/>
        <input name="enviarMissatgeTancament" type="hidden" value=""/>
        <input name="infraestructura" type="hidden" value=""/>

        <!-- boto per enviar -->
        <input type="submit" value="Envia">
        <!-- imatge que envia -->
        <script type="text/javascript">
        $("#servei2imatge").click(function(){$("#servei2form").submit()})
        </script>
        <input id="servei2imatge" type="image" onclick="servei1form.submit()" src="http://seuelectronica.upc.edu/perfil-de-contractant/imatges/imatge-per-a-contacte"/>
    </form>

.. note::

    Cal omplir el contingut del atribut *value* dels camps que es vulguin predefinir, els camps que no s'utilitzin es poden esborrar.

Formulari amb els camps ocults per a proves::

    <form method="get" action="gn6-alta-tiquet" id="servei3form">
        <input name="assumpte" type="hidden" value="Prova amb formulari i boto imatge"/>
        <!-- imatge que envia -->
        <script type="text/javascript">
        $("#servei3imatge").click(function(){$("#servei2form").submit()})
        </script>
        <input id="servei3imatge" type="image" onclick="servei1form.submit()" src="http://seuelectronica.upc.edu/perfil-de-contractant/imatges/imatge-per-a-contacte"/>
    </form>

Guia docent publica
-------------------

La integracio amb la Guia docent publica permet visualitzar les diferents guies docents amb el Genweb.

Les guies es generen cridant a la la url relativa: **guiadocent-obtenir-pdf**, amb els parametres necessaris per a trobar la guia:

    codi (obligatori): codi que identifica la unitat docent en questio
    grup (obligatori): grup de la guia d'estudis
    idioma (obligatori): valors posibles CA, ES, ENG
    curs: any de la guia docent. Ex. 2009

Exemples
++++++++

:Exemple en catala: guiadocent-obtenir-pdf?codi=14742&idioma=ca&grup=1
:Exemple en castella: guiadocent-obtenir-pdf?codi=14742&idioma=es&grup=1
:Exemple en catala i curs 2009: guiadocent-obtenir-pdf?codi=14742&idioma=ca&grup=1&curs=2009
