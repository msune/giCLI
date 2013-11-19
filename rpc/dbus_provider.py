from rpc_provider import RpcProvider
from syntax.syntax_provider import SyntaxProvider

class DbusProvider(RpcProvider):
	""" Abstract class for RPC providers"""

	def __init__(self, **kwargs):
		print "Initalizing DBUS RPC provider..."
		self.syntax_provider = SyntaxProvider.factory("LibconfigProvider")

	#Provider Interface methods
	def getAppName(self): 
		return "name"	

	def getAppInfo(self): 
		return "Info"	

	def getActions(self): 
		return [] 
	
 	def getConfiguration(self, parent, index=0):
		#FIXME: Call rpc
		rpc_string = open("rpc/example_complex.cfg", 'r').read()
		return self.syntax_provider.deserialize("", rpc_string, parent)

 	def setConfiguration(self, config, dry_run=False):
		rpc_string = syntax_provider.serialize(config)

		#FIXME: Call rpc
