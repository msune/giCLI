from scopes import Scope
import cmd

#Prototype of an action
class Root(Scope):
	""" Main interactive CLI  """ 
	#Name
	def __init__(self, rpcProvider):
		"""Constructor"""
	
		Scope.__init__(self,"root", rpcProvider, appName=rpcProvider.getAppName())
		
		#Setting a nice intro	
		self.intro = rpcProvider.getAppInfo()
	
		#Initialize main subscope (config)
		self.subScopes["config"] = rpcProvider.getConfiguration(self) 
		
		#Actions
		#FIXME
		
		#Delete unnecessary actions
		#FIXME

	#Config scope (edit mode)
	def do_config(self, s):
		"""Enters configuration mode"""

		#FIXME: authentication

		print "Entering configuration mode..."	
		ret = self.launchSubScope("config")	
		print "Leaving configuration mode"	
	
		#Must return the value!!!
		return ret

	def postloop(self):
		print "Goodbye!"
		return True

	def help_quit (self):
		print "Quits the ..."
