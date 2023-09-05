import json
import pkgutil

DATA_PATH = "./data"

def getref(key):
	path = f"{key}.json"
	return json.loads(pkgutil.get_data(__name__, f"data/{path}").decode())

genref = getref("genref")
occref = getref("occref")
skillref = getref("skillref")
spellref = getref("spellref")
weapref = getref("weapref")
itemref = getref("itemref")
topdftemp = getref("topdf")
tojsontemp = getref("tojson")
toprismtemp = getref("toprism")

def attrget(o, *args, default=None):
	if not args:
		return o 
	else:
		key, *args = args
	return rget(getattr(o, key), *args)

def rget(d, *args, default=None):
	if not args:
		return d
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

# with open("pdf_template.json") as fp:
# 	pdf_keys = json.load(fp)
# with open("json_template.json") as fp:
# 	json_keys = json.load(fp)
# with open("prism_template.json") as fp:
# 	json_keys = json.load(fp)	
# with open("create_ref.json") as fp:
# 	create_refs = json.load(fp)
# with open("occ_ref.json") as fp:
# 	occ_ref = json.load(fp)
# with open("skill_ref.json") as fp:
# 	skill_ref = json.load(fp)
# with open("weapon_ref.json") as fp:
# 	weapon_ref = json.load(fp)
# with open("item_ref.json") as fp:
# 	item_ref = json.load(fp)
# with open("spell_ref.json") as fp:
# 	spell_ref = json.load(fp)
