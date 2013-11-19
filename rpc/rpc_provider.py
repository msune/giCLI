

class RpcProvider(object):
	""" Abstract class for RPC providers"""

	def __init__(self, **kwargs):
		""" Constructor """
		raise Exception("An abstract class cannot be instantiated")	

	@staticmethod
	def factory(providerName="", **kwargs):
		#Add all providers here
		from dbus_provider import DbusProvider

		#Default
		if providerName == "":
			providerName = DbusProvider.__name__ 

		#Provider factory		
		if providerName == DbusProvider.__name__:
			return DbusProvider(*kwargs)

		raise Exception("Unsupported RPC provider") 

	#Provider Interface methods
	def getAppName(self): 
		""" Returns the (remote) application name """
		raise Exception("Not implemented")

	def getAppInfo(self): 
		""" Returns the (remote) application information """
		raise Exception("Not implemented")

	def getActions(self): 
		""" Returns the list of CLIActions """
		raise Exception("Not implemented")

 	def getConfiguration(self, parent, index=0): 
		""" 
		Returns the CLI configuratin hierarchy, filled up with
		the configuration number 'index'
		"""
		raise Exception("Not implemented")

 	def setConfiguration(self, config, dry_run=False):
 		""" 
		Attempts to set the configuration. When dry_run is True,
		the remote peer should only attempt to validate the configuration.
		"""
		raise Exception("Not implemented") 
