
__all__ = ['Session', 'UOBSession']

import warnings
import logging
from order.uob import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Session:
	def __init__(self, *args, **kws):
		"""Parser of RFC 2822 and MIME email messages.
		
		Creates an in-memory object tree representing the email message, which
		can then be manipulated and turned over to a Generator to return the
		textual representation of the message.
		
		The string must be formatted as a block of RFC 2822 headers and header
		continuation lines, optionally preceeded by a `Unix-from' header.  The
		header block is terminated either by the end of the string or by a
		blank line.
		
		_class is the class to instantiate for new message objects when they
		must be created.  This class must have a constructor that can take
		zero arguments.  Default is Message.Message.
		"""
		self._sessiontype = ''
		self._sessionValid = False
		if len(args) >= 1:
			if '_class' in kws:
				raise TypeError("Multiple values for keyword arg '_class'")
			kws['_class'] = args[0]
		if len(args) == 2:
			if 'strict' in kws:
				raise TypeError("Multiple values for keyword arg 'strict'")
			kws['strict'] = args[1]
		if len(args) > 2:
			raise TypeError('Too many arguments')
		if 'strict' in kws:
			warnings.warn("'strict' argument is deprecated (and ignored)",
						DeprecationWarning, 2)
			del kws['strict']
		if kws:
			print type(kws)
			print kws
			raise TypeError('Unexpected keyword arguments')
	
	
	def Login(self, platform):
		return False
	def SessionType(self):
		return self._sessiontype

		
class UOBSession(Session):
	def Login(self, platform):
		self._sessiontype = 'Cookie'
		self._cookie = ''
		self._cookies = None
		logger.info("Try login to platform:%s" % platform)
		try:
			ConnectToUOBWIthLogin()
			SendLoginCredentialToUOB()
			self._cookies = BrowserToPlatBrow()
		except Exception, e:
			print "Login failed. Please check"
		else:
			self._cookie = "; ".join(self._cookies)
			self._sessionValid = True
			
	def GetTodaysOrder(self):
		if not self._sessionValid:
			return None
		today_orders = GetTodaysOrder(self._cookie)
		print today_orders
		
	def GetCookie(self):
		if hasattr(self, "_cookie"):
			return self._cookie
		else:
			return None
	def PlaceOrder(self, symbol, order_type, limit, price, quntity)
		pass