
class SyntaxProvider(object):
	""" Abstract class for a serialization syntax provider"""

	def __init__(self, **kwargs):
		""" Constructor """
		raise Exception("An abstract class cannot be instantiated")	

	@staticmethod
	def factory(providerName="", **kwargs):
		#Add all providers here

		#Default
		if providerName == "":
			providerName = "LibconfigProvider"

		#Provider factory		
		if providerName == "LibconfigProvider":
			from libconfig_provider import LibconfigProvider
			return LibconfigProvider(**kwargs)

		raise Exception("Unsupported RPC provider") 

	#Provider Interface methods
 	def serialize(self, config):
 		""" 
		Serializes a config hierarchy	
		"""
		raise Exception("Not implemented")

  	def deserialize(self, configString, parent):
 		""" 
		Deserializes a config string
		"""
		raise Exception("Not implemented")

  	def dump(self, config):
 		""" 
		Returns a human readble representation of the configuration
		"""
		raise Exception("Not implemented") 
