
#Confirmation util
def confirm(msg):
	""" Util confirmation """
	ok = set(['yes','y', 'ye'])
	ko = set(['no','n', '']) #default no
	
	while 1:
		print "Are you sure %s (Y/N)?" % msg	
		aux = raw_input().lower()
		if aux in ok:
			return True
		elif aux in ko:
			return False


