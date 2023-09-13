import json
import pkgutil
import random	

DATA_PATH = "./data"

def getref(key):
	path = f"{key}.json"
	return json.loads(pkgutil.get_data(__name__, f"data/{path}").decode())

genref = getref("genref")
nameref = getref("nameref")
occref = getref("occref")
skillref = getref("skillref")
spellref = getref("spellref")
weapref = getref("weapref")
itemref = getref("itemref")
pdfref = getref("pdfref")
jsonref = getref("jsonref")
prismref = getref("prismref")

def constrainedsum(n, total):
		dividers = sorted(random.sample(range(1, total), n - 1))
		return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

def attrget(o, *args, default=None):
	if not args:
		return o 
	else:
		key, *args = args
	return rget(getattr(o, key), *args)

def rget(d, *args, default=None):
	if not args:
		return d or default
	else:
		key, *args = args 
		return rget(d.get(key), *args, default=default)

def rgetlist(d, *args, default=[]):
	if not args:
		return [d]
	else:
		key, *args = args
		if isinstance(key, list):
			return [d.get(k) for k in key]
		else:
			return(rgetlist(d.get(key, default), *args, default=default))

def svalget(obj, skill):
	attrget(obj, "skills", skill, "value")

def sanitize_keys(d):
	keys = [k.replace(" ", "").replace("/","_").lower() for k in d.keys()]
	return {k:v for k, v in zip(keys, d.values())}

def sanitize_key(k):
	return k.replace(" ", "").replace("/", "_").lower()

def trueforall(ls):
	return reduce(lambda x, y: x and y, ls)
	
def trueforone(ls):
	return reduce(lambda x, y: x or y, ls)
