import cmd

from utils import confirm


#Prototype of an action
class CLIAction(object):
	""" Abstraction for an action (RPC method)"""

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

