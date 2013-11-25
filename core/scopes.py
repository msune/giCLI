import cmd
from data_field import DataField
from exceptions import *
from utils import *

class Scope(cmd.Cmd):
	"""Scope encapsulates a scope CLI routines and fields (like configure...)"""
	
	#Shared stuff
	scopeSeparator = "."
	startScopes = "#"
	endCharacter = ">"
	
	#A Scope cannot be further navigated down
	def __init__ (self, scope, rpcProvider, parentScope=None, scopeShortCode=None, appName="gCLI"):
		"""Constructor"""
		cmd.Cmd.__init__(self)

	
		#print "Constructing scope: %s, parentScope: %s, scopeShortCode: %s, appName:%s" %(scope, parentScope, scopeShortCode, appName)
		self.APP_NAME = appName #Must be defined by the inherited constructor of the very first scope
		self.scope = scope #inherited elements MUST define this
		self.parent = parentScope 
		self.rpcProvider = rpcProvider
		
		#Other	
		if scopeShortCode:
			self.scopeShortCode = scopeShortCode 
		else:
			self.scopeShortCode = self.scope 

		if self.parent and self.parent.prompt:
			self.prompt = self.parent.prompt[:-1]
			if self.parent.prompt[-2] != self.startScopes:
				self.prompt += self.scopeSeparator
			self.prompt += self.scopeShortCode+self.endCharacter
		else:
			#Very initial
			self.prompt = self.APP_NAME+self.startScopes+self.endCharacter
	
		#print "Prompt: %s is %s" % (self, self.prompt)	

		#Containers
		self.fields = dict() 
		self.subScopes = dict() 

	def addSubScope(self, obj):
		if not isinstance(obj, Scope):
			raise Exception("Unknown type")
	
		#Add method at runtime
		try:
			auto ="def do_%s(self, *args):\n\tself.launchSubScope(\"%s\")"%(obj.scopeShortCode, obj.scopeShortCode) 
			exec(auto, globals(), self.__dict__)
			fn = eval("self.do_%s"%obj.scopeShortCode)
			setattr(self.__class__, fn.__name__, MethodType(fn, self, self))
			setattr(self, fn.__name__, MethodType(fn, self, self))
			#setattr(Scope, fn.__name__, fn.__name__ )
		except Exception,e:
			print "COULD not execute code: %s"%str(e)


		#Add to the list of subscopes
		self.subScopes[obj.scopeShortCode] = obj

	#Setter and getter field for the scope
	def setField(self, field):
		"""Sets a field to the value pointed by field. Field must be a DataField"""
			
		if not isinstance(field, DataField):
			raise Exception("Unknown type")
		
		#Insert to the fields list (override if existing)
		self.fields[field.name] = field

	def getField(self, name):
		"""Retrieves the value of the field named @name"""
		return self.fields[name].value

	#Common commands(Navigation)	
	def do_quit (self, s="", noConfirmation=False):
		"""Quits the CLI"""
		if noConfirmation:
			return True	
		if confirm("you want to quit from the application"):
			if self.parent:	
				raise Quit()
			return True
	def help_quit(self):
		print "Quits the %s CLI." % self.APP_NAME 

	def do_exit (self, name=""):
		"""Exits subScope"""
		if confirm("you want to exit from %s without saving"%(self.scope)):	
			return True
	def help_exit(self):
		print "Exit from 'config' mode." % self.scope #Inhertied classes MUST define scope name	

	#Other useful stuff
	def do_show(self,s=""):
		"""Shows current scope contents"""
		pass

	def help_show(self):
		print "Shows current scope contents"

	#necessary for \n
	def emptyline(self, s=""):
		"""Do nothing..."""
		pass

	#Catches inner run-time added subscopes
	def default(self, line):
		print "Unknown command: '%s'"%line

	#Catches complete, and adds run-time added subscopes
	def complete_cmd(self, text, line, start_index, end_index):
		if text:
			return [command for command in commands
				if command.startswith(text)]
		else:
			return commands

	#Sub-scope launching routine
	def launchSubScope(self, name):
		"""Launches a sub-scope within the current one"""
		#print str(self)+"Trying to launch: %s" % name
		try:
			self.subScopes[name].cmdloop()
		except KeyboardInterrupt:
			self.subScopes[name].do_exit(None)
		except UpScope, e:
			pass
		except TopScope, e:
			if self.canNavigateUp:
				raise e
		except Exit, e:
			if not self.canNavigateUp:
				return True 
			raise e
		except Quit, e:
			if not self.parent:
				return self.do_quit(noConfirmation=True)
			raise e
			 
	
class NavigationalScope(Scope):
	"""NavigationalScope encapsulates a navigational (up/top) scope CLI"""
	
	def __init__ (self, scope, rpcProvider, parentScope=None, scopeShortCode=None, appName="gCLI", canNavigateUp=True):
		"""Constructor"""
		Scope.__init__(self, scope, rpcProvider, parentScope=parentScope, scopeShortCode=None, appName=appName)
		self.canNavigateUp = canNavigateUp

	##
	## Navigational commands
	##	
	def do_up(self, s=""):
		"""Returns to the parent scope"""
		if self.canNavigateUp:
			raise UpScope() 	

	def help_up(self,s=""):
		print "Returns to the parent scope"

	def do_top(self, s=""):
		"""Returns to the top most scope"""
		if self.canNavigateUp:
			raise TopScope()

	def help_top(self,s=""):
		print "Returns to the top most scope"
	
