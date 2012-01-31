Introducció
============

Que ofereix
-----------

La integració amb el Gestor de serveis integra la creació de tiquets des de el Genweb preomplint alguns camps per automàtizar el procés. Per crear els tiquets s'ofereixen dues opcions: una que permet a l'usuari editar el contingut d'algun dels camps del tiquet i l'altre que és completament transparent a l'usuari.


Configuració
------------

Quan s'instala el paquet per primer cop crea una configuració buida que s'ha d'omplir per poder connectar-se al `bus SOA` i al `Gestor de Serveis`, els paràmetres d'aquesta configuració són:

:gn6_user: usuari del Gestor de serveis.
:gn6_password: contrasenya de l'usuari del Gestor de serveis.
:gn6_domain: domini del Gestor de serveis.
:bussoa_user: usuari del bus SOA.
:bussoa_password: contrasenya de l'usuari del bus SOA.
:wsdl_gestiotiquets: url al fitxer wsdl del gestor de tiquets.


.. note::

	L'*usuari del gestor de serveis* s'ha de demanar a la persona que gestiona el **Gestor de serveis**.

.. note::

	L'*usuari del bus SOA* s'ha de demanar al **Govern SOA** i ha d'autoritzar les màquines que s'hi connectin.


Demanar accés al BUS SOA
++++++++++++++++++++++++

Les màquines que utilitzin aquest servei s'han de donar d'alta al contracte del servei web amb el Govern SOA.



Filtratge HTML
++++++++++++++
* Recomanat *

Per poder afegir els enllaços utitlizan formularis cal permetre les etiquetes `form` i `input` a la configuració del *Filtratge Html*.

* Proves *

El formulari de proves utlitza les etiquetes `select` i `option` per generar els desplegables.



Demanar informació a l'usuari
-----------------------------

Una de les vistes del paquet permet generar enllaços que g


Generació dels enllaços per crear tiquets
-----------------------------------------

Per generar els enllaços per creat tiquets hi han dues opcions: `<form/>` o `<a/>`; les dues opcions porten al mateix resultat final, però cadascuna té els seus pros i contres.

**Enllaç**

*Pros*

- Fàcil de crear i personalitzar: ideal si es vol fer que l'enllaç sigui una imatge.
- No s'ha de modificar la configuració per defecte del Genweb.

*Contras*

- Poc administrable si es defineixen molts paràmetres.


**Formulari**

*Pros*

- Gestió dels paràmetres més fàcil

*Contras*

- Si es vol enviar l'informació al clicar a una imatge cal javascript.
- S'ha de modificar la configuració per defecte del Genweb.


Code snippets
-------------

Enllaç
++++++

Enllaç amb assumpte de prova::

	<a href="gn6-alta-tiquet?assumpte=Prova+amb+href">
		<img src="http://seuelectronica.upc.edu/perfil-de-contractant/imatges/imatge-per-a-contacte"/>
	</a>

Formulari
+++++++++

El codi següent es un formulari que permet fer proves i generar url's valides::

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


		Enviar Creació<input name="enviarMissatgeCreacio" type="text" /> <br />Enviar Tancament<input name="enviarMissatgeTancament" type="text" /> <br />Infraestructura<input name="infraestructura" type="text" /> <br />


		<!-- TEST MODE: no fa l'alta, només fa una validació parcial de la petició -->
        Mode proves (no crea el tiquet):
		<input type="checkbox" name="test" value="1"/>
		<!-- FI TEST MODE -->
		<!-- boto per enviar -->
		<input type="submit" value="Envia">
	</form>

Formulari amb els camps ocults per a ús d'usuari final::

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

		<!-- TEST MODE: no fa l'alta, només fa una validació parcial de la petició -->
		<input type="checkbox" name="test" value="1"/>
		<!-- FI TEST MODE -->
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
	 	<input name="assumpte" type="hidden" value="Prova amb formulari i botó imatge"/>
		<!-- imatge que envia -->
		<script type="text/javascript">
		$("#servei3imatge").click(function(){$("#servei2form").submit()})
		</script>
		<input id="servei3imatge" type="image" onclick="servei1form.submit()" src="http://seuelectronica.upc.edu/perfil-de-contractant/imatges/imatge-per-a-contacte"/>
	</form>

**Com funciona la imatge**

.. TODO


Proves: URI's incorrectes
-------------------------

Les següents URI's han de redireccionar i mostrar un error al executar-se:

#. Sense cap parametre::

	http://localhost:8080/Plone/gn6-alta-tiquet

#. Assumpte buit pero a la petició::

	http://localhost:8080/Plone/gn6-alta-tiquet?assumpte=

#. Proces incorrecte::

	http://localhost:8080/Plone/gn6-alta-tiquet?assumpte=Prova&proces=MALO
