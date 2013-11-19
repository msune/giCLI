import cmd
import readline
from types import MethodType, ClassType

from utils import confirm

#Useful exceptions for navigation
class Quit(Exception):
	pass
class Exit(Exception):
	pass
class UpScope(Exception):
	pass
class TopScope(Exception):
	pass


##
## Scoped CLI abstractions
##

class DataField(object):
	""" Abstraction for a data field """

	def __init__(self, name, value):
		self.name = name
		self._type = type(value)
		self.value = value
	
	def __str__(self):
		return "[%s,%s,%s]"%(name, str(_type), str(value))

	def serialize(self, prefix):
		if str(self.value) != "":
			return prefix+self.name+" = "+str(self.value)+";\n"
		return ""


class CLIScope(cmd.Cmd):
	"""CLIScope encapsulates a scope CLI routines and fields (like configure...)"""
	
	#Shared stuff
	CLIscopeSeparator = "."
	CLIstartScopes = "#"
	CLIendCharacter = ">"
	
	#A CLIScope cannot be further navigated down
	def __init__ (self, scope, parentScope=None, scopeShortCode=None, appName=None, canNavigateUp=True):
		"""Constructor"""
		cmd.Cmd.__init__(self)
		
		#print "Constructing: %s, %s, %s, %s" %(scope, parentScope, scopeShortCode, appName)
		self.APP_NAME = appName #Must be defined by the inherited constructor of the very first scope
		self.scope = scope #inherited elements MUST define this
		self.parent = parentScope 
		self.canNavigateUp = canNavigateUp
		
		#Other	
		if scopeShortCode:
			self.scopeShortCode = scopeShortCode 
		else:
			self.scopeShortCode = self.scope 
		
		if self.parent and self.parent.prompt:
			self.prompt = self.parent.prompt[:-1]
			if self.parent.prompt[-2] != self.CLIstartScopes:
				self.prompt += self.CLIscopeSeparator
			self.prompt += self.scopeShortCode+self.CLIendCharacter
		else:
			#Very initial
			self.prompt = self.APP_NAME+self.CLIstartScopes+self.CLIendCharacter
		

		#Containers
		self.fields = dict() 
		self.subScopes = dict() 

	#def do_interfaces(self, *args):
	#	print self 
	#	self.launchSubCLIScope("interfaces")

	def addSubScope(self, obj):
		if not isinstance(obj, CLIScope):
			raise Exception("Unknown type")
	
		#Add method at runtime
		try:
			auto ="def do_%s(self, *args):\n\tself.launchSubCLIScope(\"%s\")"%(obj.scopeShortCode, obj.scopeShortCode) 
			exec(auto, globals(), self.__dict__)
			fn = eval("self.do_%s"%obj.scopeShortCode)
			setattr(self.__class__, fn.__name__, MethodType(fn, self, self))
			setattr(self, fn.__name__, MethodType(fn, self, self))
			#setattr(CLIScope, fn.__name__, fn.__name__ )
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
		print "Quits the %s." % self.APP_NAME 

	#def do_up(self, s=""):
	#	"""Returns to the parent scope"""
	#	pass # This is not navigational scope
	#def help_up(self,s=""):
	#	print "Returns to the parent scope"

	#def do_top(self, s=""):
	#	"""Returns to the top most scope"""
	#	pass # This is not a navigational scope
	#def help_top(self,s=""):
	#	print "Returns to the top most scope"
	
	def do_exit (self, name=""):
		"""Exits subScope"""
		if confirm("you want to exit from %s without saving"%(self.scope)):	
			return True
	def help_exit(self):
		print "Exit from %s mode." % self.scope #Inhertied classes MUST define scope name	

	#Other useful stuff
	def do_show(self,s=""):
		"""Shows current scope contents"""
		print self.serialize()
	def help_show(self):
		print "Shows current scope contents"

	#necessary for \n
	def emptyline(self, s=""):
		"""Do nothing..."""
		pass

	#Catches inner run-time added subscopes
	def default(self, line):
		#Look for a valid command
		#cmd = line.split(' ', 1)[0]
 		#for scope in self.subScopes:
		#	if scope == cmd:
		#		self.launchSubCLIScope(scope)	
		#		return	
		#if cmd:	
		print "Unknown command: '%s'"%line

	#Catches complete, and adds run-time added subscopes
	def complete_cmd(self, text, line, start_index, end_index):
		print "hallo"
		if text:
			return [command for command in commands
				if command.startswith(text)]
		else:
			return commands

	#Sub-scope launching routine
	def launchSubCLIScope(self, name):
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
			 
	#Scope serialization and deserialization
	def serialize(self, linePrefix=""):
		"""Serializes the scope"""
		
		serial = linePrefix+self.scope+":{\n"
		#First serialize fields
		for elem in self.fields.values():
			serial += elem.serialize(linePrefix+"\t")
		#Serialize subscopes
		for ss in self.subScopes.values():
			serial += ss.serialize(linePrefix+"\t")
		#Close scope
		serial += linePrefix+"}\n"
		return serial 

	def deserialize(self, string):
		TODO
		pass	
		
	##Register field types and 


class NavigationalCLIScope(CLIScope):
	"""NavigationalCLIScope encapsulates a navigational (up/top) scope CLI"""
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
	
	


