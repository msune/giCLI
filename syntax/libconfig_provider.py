from syntax_provider import SyntaxProvider
from core.config import CLIConfig
from pylibconfig import Config 

class LibconfigUtils(object):
	
	@staticmethod
	def serialize(config):
		return ""	

class LibconfigProvider(SyntaxProvider):
	"""
	libconfig-based syntax provider
	"""

	def __init__(self, **kwargs):
		pass

	#Provider Interface methods
 	def serialize(self, config):
		return LibconfigUtils.serialize(config) 

  	def deserialize(self, schema, configString, parent):

		#Parse libconfig string
		lconf = Config()
		lconf.readString(configString)

		#Build the basic structure 		
		config = CLIConfig(parent) 

		#Read values
		#FIXME
	
		return config
 
  	def dump(self, config):
		return "dump of the config: "+LibconfigProvider.serialize(config)
