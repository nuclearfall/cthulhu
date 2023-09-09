from roll import dunits
from refs import *


DATASTRUCT = {
	"imports": ["random"],
	"function": lambda *x, **y: dunits(*x, **y),
	"ordparams": [2],
	"defparams": {
		"highval": 12,
		"fn": sum,
		"count": 3},
	"ref": skillref,
}


def createstruct(fn, *args, **kwargs):
	_dict = {"function":fn, "ordparams": args,
			"defparams": kwargs}

def structfromfunction():
	pass

def rgetlist(d, *args, default=[]):
	if not args:
		return [d]
	else:
		key, *args = args
		if isinstance(key, list):
			return [d.get(k) for k in key]
		else:
			return rgetlist(d.get(key, default), *args, default=default)

### define all function within data structure
def fnfromstruct(datastruct):
	imports, function, ref, opar, defp = rgetlist(datastruct, 
				["imports", "function", "ref",  "ordparams", "defparams"])
	[exec(f"import {x}") for x in imports]
	return function(*opar, **defp)

def fnfromstuct(datastruct):
	opar, defp = rgetlist(datastruct, 
				["function", "variables", "ordparams", "defparams"])
print(fnfromstruct(DATASTRUCT))

