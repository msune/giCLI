#!/usr/bin/env python

from core.root import CLIRoot
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
	cli = CLIRoot(provider)

	#Loop	
	try:
		cli.cmdloop()
	except KeyboardInterrupt:
		cli.do_quit(None)


