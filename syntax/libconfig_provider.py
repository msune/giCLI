from syntax_provider import SyntaxProvider
from core.scopes import NavigationalScope 
from pylibconfig import Config 
from lxml import etree

class LibconfigUtils(object):
	
	@staticmethod
	def serialize(config):
		return ""	

	@staticmethod
	def parseSchemaScope(schema, config, prefix=""):
		for schemaChild in schema.iterchildren():
			#print prefix+str(schemaChild)
			if schemaChild.get("name"):
				print "Name: %s type:%s tag:%s\n" % (schemaChild.get("name"), schemaChild.get("type"), schemaChild.tag)
			LibconfigUtils.parseSchemaScope(schemaChild, config, prefix+"\t")

	@staticmethod
	def generateEmptyConfig(schema, parent, rpcProvider, appName):
		#xmlschema = etree.XMLSchema(etree.XML(schema))
		xmlschema = etree.fromstring(schema)
		#xsd = etree.fromstring(schema)
		#xmlschema = etree.XMLSchema(xsd)
		config = NavigationalScope("config", rpcProvider, parentScope=parent, appName=appName, canNavigateUp=False) 

		LibconfigUtils.parseSchemaScope(xmlschema, config)	

		return config

class LibconfigProvider(SyntaxProvider):
	""" libconfig-based syntax provider """

	def __init__(self, **kwargs):
		self.rpcProvider = kwargs["rpcProvider"]
		self.appName = kwargs["appName"]

	#Provider Interface methods
 	def serialize(self, config):
		return LibconfigUtils.serialize(config) 

  	def deserialize(self, configString, parent):

		#Parse libconfig string
		lconf = Config()
		lconf.readString(configString)

		#Schema
		schema = self.rpcProvider.getConfigurationSchema()

		#Build the basic structure 		
		config = LibconfigUtils.generateEmptyConfig(schema, parent, self.rpcProvider, self.appName)

		#Read values
		#FIXME
	
		return config
 
  	def dump(self, config):
		return "dump of the config: "+LibconfigProvider.serialize(config)
