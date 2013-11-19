from scopes import CLIScope, NavigationalCLIScope, DataField

class ConfigField(DataField):
	""" Abstraction for a config data field """
	pass

class CLIConfig(NavigationalCLIScope):
	""" Main configuration scope CLI"""
	def __init__(self, parentScope):
		CLIScope.__init__(self, "configuration", parentScope=parentScope, scopeShortCode="config", canNavigateUp=False)
		self.intro = "Entering configuration mode..."
		try:
			#Add fields	
			self.setField(ConfigField("debug","None"))
				
			#Add subScopes...
			#import interfaces.interfaces as interfaces
			#import openflow.logical_switches as logical_switches
			#self.addSubScope(interfaces.interfaces(self))
			#self.addSubScope(logical_switches.logical_switches(self))

		except Exception,e:
			print "COULD not add subscope or field: %s"%str(e)

	def do_dump(self, s=""):
		try:
			print self.serialize()
		except Exception,e:
			print str(e)

	#Postloop message
	def postloop(self):
		print "Leaving %s mode." % self.scope #Inhertied classes MUST define scope name	


class SubCLIConfig(NavigationalCLIScope):
	"""Main configuration sub scope CLI. No confirmation for exit."""
	
	def __init__(self, scope, parentScope):
		CLIScope.__init__(self, scope, parentScope)
		self.intro = None
 
	def do_exit(self, name):
		return True
	
	def postloop(self):
		pass	


