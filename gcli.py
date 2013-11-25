#!/usr/bin/env python

from core.root import Root
from core.exceptions import Quit
from rpc.rpc_provider import RpcProvider 

##
## Main routine
##
if __name__ == "__main__":
	print "Welcome to GCLI"

	#Instantiate provider
	#FIXME 
	provider = RpcProvider.factory()

	#Generate cli object
	cli = Root(provider)

	#Loop	
	try:
		cli.cmdloop()
	except Quit, KeyboardInterrupt:
		cli.do_quit(None)


