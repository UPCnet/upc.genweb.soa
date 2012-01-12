# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

from upc.genwebCBL.gn6 import GN6_GestioTiquets
from upc.genwebCBL.gn6_properties import GN6_Properties

class AltaTiquetView(BrowserView):

	__call__ = ViewPageTemplateFile('altaTiquet.pt')
	    
	def __init__(self, context, request):
		self.context = context
		self.request = request
	
	def _get_user(self):
		"""Retorna l'usuari quue esta autenticat al portal"""
		mt = getToolByName(self.context, 'portal_membership')
		if mt.isAnonymousUser(): # the user has not logged in
			return None
		else:
			return mt.getAuthenticatedMember()
    
	def _get_ip(self):		
	    """ Extract the client IP address from the HTTP request in a proxy-compatible way.
	    from: http://collective-docs.readthedocs.org/en/latest/serving/http_request_and_response.html#request-client-ip
	    @return: IP address as a string or None if not available
	    """
	    if "HTTP_X_FORWARDED_FOR" in self.request.environ:
	        # Virtual host
	        ip = self.request.environ["HTTP_X_FORWARDED_FOR"]
	    elif "HTTP_HOST" in self.request.environ:
	        # Non-virtualhost
	        ip = self.request.environ["REMOTE_ADDR"]
	    else:
	        # Unit test code?
	        ip = None	    
	    return ip
			

	def _get_portal_url(self):
		""" Retorna l'adreça del portal """
		urltool = getToolByName(self.context, 'portal_url')
		portal = urltool.getPortalObject()		
		return portal.absolute_url()
	
	def _redirect(self):
		""" Redirecciona a la pàgina d'on venia l'usuari o a la pàgina 
		principal si el valor no està definit (HTTP_REFERER)"""				
		redirect = self.request.get('HTTP_REFERER');		
		if redirect is None or redirect == '':
			redirect = self._get_portal_url()		
		# Redirecció
		self.request.response.redirect(redirect)
	
	def _error(self, missatge):
		"""Acaba la petició redireccionant i mostrant un missatge d'error"""
		self.context.plone_utils.addPortalMessage(missatge, 'error')
		self._redirect(missatge)
		#TODO exit?
		
	def alta(self):
		import ipdb; ipdb.set_trace()
		gn6_prop =  GN6_Properties(self.context)
		p = gn6_prop.get_all()
		# Obtenim l'usuari i comprovem l'usuari
		user = self._get_user()		
		if user is None:
			self.error(_('Permissos insuficients'))
			return
		
		# Comprovem que el GW estigui configurat per treballar amb el GN6
		if p['gn6_user'] == '':
			self.error(_("No s'ha configurat el Gestor de Serveis"))
			return
		
		g = GN6_GestioTiquets(p['gn6_user'], p['gn6_password'], p['gn6_domain'], p['bussoa_user'], p['bussoa_password'])
		
		# Obtenim els parametres de la petició
		f = self.request.form
		if 'test' in f:
			g.mode_test()
		# Hi han parametres no modificables amb el formulari, els esborrem de la crida
		desactivats = ['estat', 'ip', 'solicitant', 'client']
		for a in desactivats:
			if a in f:
				del f[a]
		
		#TODO Sanitize?

		# Camps que fixats
		#TODO Potser seria millor self.request.getClientAddr()?
		f['ip'] = self._get_ip()
		f['solicitant'] = user.getId();		

		# Cridem a l'alta al gestor
		t = g.alta_tiquet(f)
		
		# Processem el retorn
		response = self.request.response
		if g.resultat_ok():
			missatge = _("S'ha creat un tiquet amb identificador ${codi}",mapping={'codi': t.codiTiquet})
			self.context.plone_utils.addPortalMessage(missatge, 'info')
		else:			
			self.context.plone_utils.addPortalMessage(g.ultim_error(), 'error')			
		self._redirect()
		return