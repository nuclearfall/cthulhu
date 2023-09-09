import refs
import roll
import pickle
from pprint import pprint

PRIMARY = ["pow", "str", "con", "dex", "app", "siz", "edu", "int"]
SECONDARY = ["mov", "db", "build", "hp", 
        "hp", "mp", "sanity", "max_sanity", "dodge"]
# PRIMARY3D6 = ["str", "con", "dex", "app", "pow", "luck"]
# PRIMARY2D6P6 = ["int", "edu", "siz"]
path = "./data/primarychars.pyth"
charref = pickle.load(open(path, "rb"))

_dbbuild = {
		range(2,65): {
			"build": -2,
			"db": "-2"
		},
		range(65, 85): {
			"build": -1,
			"db": "-1"
		},
		range(85, 125): {
			"build": 0,
			"db": "0"
		},
		range(125, 165): {
			"build": 1,
			"db": "1d4"
		},
		range(165, 204): {
			"build": 2,
			"db": "1d6"
		}
	}
def character_template():
	return refs.jsonref
def occs():
	return refs.occref
def skills():
	return refs.skillref

def dapply(character, mods, fn=sum):
	for k, m in mods.items():
		if character.get(k):
			character[k] = fn(character[k], m)
	return character

#### PRIMARY CHARACTERISTICS AND LUCK ####
def withrolledchars(genref=charref):
	temp = character_template()
	for k, v in genref.items():
		temp[k] = roll.dunits(**v)
	return temp

#### AGE AND AGING (TO GO SOMEWHERE ELSE) ####
def teenage_development(character, changes):
	if character.get("age") not in range(15, 20):
		return character
	dapply(changes, character, lambda x, y: x-y)
	return {**character, **{"edu": character.get("edu")-5}}

def nowofage(teenager, changes):
	dapply(changes, character, lambda x, y: x+y)
	teenager += improvement_check(teenage.get("edu"))
	return teenager

def outofprime_choicecalc(value, base=30, step=5):
	return int(pow(2, int((value - base) / 10)-1) * step)

def outofprime_appadj(value, base=30):
	return int((value - base) / 2)

def educheck_count(age, base=30):
	return int((age - 30) / 10)

def is_changes_valid(value, changes, keys=["str", "dex", "con"]):
	#print(value, changes)
	correct_keys = [k for k in changes.keys() if k in keys]
	correct_sum = abs(sum([v for v in changes.values(
				)])) == outofprime_choicecalc(value)
	return True if correct_keys and correct_sum else False

def outofprime_adj(character, changes={}):
	if is_changes_valid(character.get("age"), changes):
		adjusted = dapply(character, changes, fn=lambda x, y: x-y)
		return adjusted
	else:
		raise ValueError(f"{changes} are invalid for age: {character.get('age')}")

def outofprime(character, changes):
	if character.get("age") in range(15, 40):
		return character
	character = improvement_check(educheck_count(character.get("age")))
	for k, v in changes.items():
		character = k(character, **v)
	character["app"] -= outofprime_appadj(character.get("age"))
	return character

#### Set all secondary chars now that age adjustments are out of the way.

def dbbuild(char, ref=_dbbuild):
	strsiz = char.get("str") + char.get("siz")
	refval = [v for k, v in ref.items() if strsiz in k][0]
	return {**char, **refval}



# def secondarychars(char, **kwargs):
# 	for k, v in kwargs.items():
# 		char = k(char, **v)
# 	return char

#### Character functions used during generation ####
def improvement_check(char, key="edu", count=1):
	if not count:
		return char
	success = [d for d in roll.dunits(highval=100, count=3, fn=list) if char.get(key) < d]
	return {**char, **{key: roll.dunits(count=len(success), fn=sum)}}

def chargen(**kwargs):
	passargs = kwargs.get("passargs", {})
	char = withrolledchars()
	for k, v in kwargs.items():
		if k in character_template().keys():
			char[k] = v
	for fn, args in passargs.items():
		char = fn(char, **args)
	return char

def ppfields(_dict, *fields):
	pprint({k:v for k, v in _dict.items() if k in fields})

if __name__ == "__main__":
	agechanges = {
		teenage_development: {"changes": {"str": 0, "siz": 0}},
		outofprime_adj: {"changes": {"str": 5, "con": 4, "dex": 1}}}
	inv = chargen(name="George", occupation="Spy", age=53, passargs=agechanges)
	#pprint(inv)
	#pprint(dbbuild(inv))
	
	ppfields(dbbuild(inv), "db", "build", "age", "edu", "str", "con", "dex")
	#pprint([(k, v) for k, v in inv.items() if k in PRIMARY or k in ["age","name","occupation"]])



		




# def tweakref(data, path):
# 	moreref_charref = {
# 		improvement_check: {"key": "edu", "count": 0}, 
# 		outofprime_adj: {"changes": {"str": 2, "con": 4}}}







