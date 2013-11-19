from scopes import CLIScope

#Prototype of an action
class CLIRoot(CLIScope):
	""" Main interactive CLI  """ 
	#Name
	def __init__ (self, rpcProvider):
		"""Constructor"""
		CLIScope.__init__(self, "CLI root", appName=rpcProvider.getAppName())
	
		#Setting a nice intro	
		self.intro = rpcProvider.getAppInfo()
	
		#Initialize main subscope (config)
		self.subScopes["config"] = rpcProvider.getConfiguration(self) 
		
		#Actions
		#FIXME

	#Config scope (edit mode)
	def do_config(self, s):
		"""Enters configuration mode"""
		#Must return the value!!!
		return self.launchSubCLIScope("config")

	def postloop(self):
		print "Goodbye."
		return True

	def help_quit (self):
		print "Quits the CLI..."

	def __str__(self):
		return "[%s,%s,%s]"%(name, str(_type), str(value))

