import refs
import roll
import pickle
import random
import json
from functools import reduce
from pprint import pprint
from copy import deepcopy

PRIMARY = ["pow", "str", "con", "dex", "app", "siz", "edu", "int"]
SECONDARY = ["luck", "mov", "db", "build", "hp", 
        "hp", "mp", "sanity", "max_sanity", "dodge"]
# PRIMARY3D6 = ["str", "con", "dex", "app", "pow", "luck"]
# PRIMARY2D6P6 = ["int", "edu", "siz"]
path = "./data/genref.pkl"
genref = pickle.load(open(path, "rb"))
#### Helper functions.
def character_template():
	return refs.jsonref
def occs():
	return refs.occref
def skills():
	return refs.skillref

def istruelist(_list):
	return reduce(lambda x, y: True if x is True and y is True else y, _list)

def dapply(character, mods, fn=sum):
	for k, m in mods.items():
		if character.get(k):
			character[k] = fn(character[k], m)
	return character

def allskillchildren(skilllist=[], ref=refs.skillref):
	[rget(refs.skillref, k, "children") for k, v in skilllist or refs.skillref.items()]

def getskillval(source, key):
	return refs.rget(source, key, "value") if refs.rget(source, key) else None

def getskill(source, key, ref=False):
	return refs.rget(source, key)

def getskills(source, *keys):
	return refs.reflist(source, keys)

def getskillsandkeys(source, skillkeys, valkeys):
	for k, v in source.items():
		if k in skillkeys:
			skills[k] = {vk: v.get(vk) for vk in valkeys}
	return skills
	#return {{sk: {vk: refs.rget(source, sk, vk) for vk in valkeys} for sk in skillkeys}}

	#return {{k: {k[v], rget(v, valkey)} for k, v in source.items() for keyval in valkeys}

def setskills(char, skillnames=[], skillvalues=[], skills={}):
	for k, v in zip(skillnames, skillvalues):
		skills[k] = v
	return {**char, **skills}


#### 1. PRIMARY CHARACTERISTICS AND LUCK ####
def withrolledchars():
	return {**character_template(), **roll.statroll()}


#################################################
#### 2. AGE AND AGING (TO GO SOMEWHERE ELSE) ####
#################################################
def teenage_development(char, changes):
	if char.get("age") not in range(15, 20):
		return char
	dapply(changes, char, lambda x, y: x-y)
	return {**char, **{"edu": char.get("edu")-5}}

def comeofage(char, changes):
	dapply(changes, char, lambda x, y: x+y)
	teenager += improvement_check(char.get("edu"))
	return char

def outofprime_choicecalc(age=30, base=30, step=5):
	return int(pow(2, int((age - base) / 10)-1) * step)

def outofprime_appadj(age=30, base=30):
	return int((age - base) / 2)

def educheck_count(age=30, base=30):
	return int((age - 30) / 10)

def ischangesvalid(age, changes, keys=["str", "dex", "con"]):
	correct_keys = [k for k in changes.keys() if k in keys]
	correct_sum = abs(sum([v for v in changes.values(
				)])) == outofprime_choicecalc(age)
	return True if correct_keys and correct_sum else False

# def outofprime_adj(char, changes={}):
# 	if ischangesvalid(char.get("age"), changes):
# 		char = dapply(char, changes, fn=lambda x, y: x-y)
# 		return char
	

def outofprime(char, changes):
	if char.get("age") in range(15, 40):
		return char
	if ischangesvalid(char.get("age"), changes):
		char = dapply(char, changes, fn=lambda x, y: x-y)
		char["app"] -= outofprime_appadj(char.get("age"))
		return char
	else:
		raise ValueError(f"{changes} are invalid for age: {character.get('age')}")



##### 3. Set all secondary chars now that age adjustments are out of the way.

def secondarychars(char):
	chars = {
		"hp": int((char.get("con")+char.get("siz")) / 10),
		"currenthp": int((char.get("con")+char.get("siz")) / 10),
		"mp": int(char.get("pow") / 5),
		"sanity": char.get("pow"), 
		"startsanity": char.get("pow"),
		"maxsanity": 99,
		"dodge": int(char.get("dex")/2)}

	return {**char, **dbbuild(char), **chars}

def dbbuild(char, ref=genref.get("dbbuild")):
	strsiz = char.get("str") + char.get("siz")
	refval = [v for k, v in ref.items() if strsiz in k]
	return refval[0]


#### Character functions used during generation ####
def improvement_check(char, key="edu", count=1):
	if char.get("age") in range(15, 20):
		return char
	if char.get("age") in range(40, 100):
		count = educheck_count(char.get("age"))
	success = [d for d in roll.dunits(highval=100, count=3, fn=list) if char.get(key) < d]
	return {**char, **{key: roll.dunits(count=len(success), fn=sum)}}



###########################
#### 4. Set Occupation ####
###########################

def setoccupation(char, ref=refs.occref, mincredit=True):
	return char.get("occupation", random.choice([o for o in ref.keys()]))

def occskillpointscenarios(char, ref=refs.occref, best=[]):
	scenarios = refs.rget(ref, char.get("occupation"), "scenarios")
	for scenario in scenarios:
		best.append(sum([char.get(key)*val for key, val in scenario.items()]))
	return max(best)

#################################################################
#### 5. Set skills. Start random assignment as it is easier. ####
#################################################################

def invalidoccskill(char, choices:list, points, ref=refs.occref):
	skills = refs.rget(ref, char.get("occupation"), "skills") + ["Credit Rating"]
	options = refs.rget(ref, char.get("occupation"), "selections")
	for index, choice in enumerate(choices):
		if not istruelist([True for i, _ in enumerate(
					choice) if isinexpandedoptions(choice.get("name"), options[i])]):
			return True
	return False

def isinexpandedoptions(skillname, option, optlist=[]):
	if skillname == "Any":
		return True if skillname in [name for name in refs.skillref.keys()] else False
	for skillname in option:
		children = refs.rget(refs.skillref, skillname, "children")
		if children:
			optlist += [skname for skname in option if refs.rget(refs.skillref, skillname, "children")]
		optlist.append(skillname)
	return True if skillname in optlist else False

def invalidpointassignment(choices:list, points):
	return not sum([choice.get("value") for choice in choices]) == points

def istransferable(skillname, value, transferable=False):
	return transferable and (value >= 50 or value >= 90) and skillname in allskillchildren(
				skill_list=["Firearms", "Fighting", "Survival", "Other Languages"])

#### TODO: define to allow 10% transfer to all associated skills in parent children.
def transferableskills(char, skill):
	return char

def setstatbasedskills(char):
	(dkey, dval), (olkey, olval) = ("Dodge", int(char.get("dex")/2)), ("Own Language", char.get("edu"))
	return {dkey: {"value": dval, "checked": False}, olkey: {"value": olval, "checked": False}}

def getcharskillval(char, skillname, ref=refs.skillref):
	charskill = refs.rget(char, "skills", skillname, "value") if char.get("skills").get(skillname) else 0
	skillskill = refs.rget(ref, skillname, "value", default=0)
	return charskill or skillskill

def iscommonskill(char, key, skill, era=0, ref=refs.occref):
	return skill.get("era") == era and (key in refs.rget(ref, char.get(
				"occupation"), "skills") or not skill.get("Uncommon")) and not skill.get("parents")

def initskills(char, era=0):
	charskills = char.get("skills")
	allskills =  {k:v for k, v in refs.skillref.items() if k in refs.pdfref.values()}
	for key, val in allskills.items():
		if iscommonskill(char, key, val):
			charskills = {**charskills, **{key: {"value": getcharskillval(char, key), "checked": False}}}
	char = {**char, **{"skills": {**charskills}}}
	return charskills

def selectskills(char, skills, skillpoints, choices=[], maxskillval=99, transferable=False):
	if invalidpointassignment(choices, skillpoints):
		raise ValueError(f"Assignments do not equal skillpoints. Ensure total is exactly {skillpoints}")
	for choice in choices:
		(nk, name), (vk, val) = choice.items()
		baseval = getcharskillval(char, name)
		if val + baseval > maxskillval:
			raise ValueError(f"Point assignment of {value} + initial value of {baseval} for {name} with would exceed {maxskillval}")
		if skills.get("name"):
			skills[name] += val
		else:
			skills[name] = {"name": name, "value":val+baseval}
		if istransferable(name, baseval+val, transferable=transferable):
			skills = transferableskills(char, skill)
	return skills

def selectoccskills(char, choices, maxskillval=99, transferable=False, mincredit=True):
	skillpoints = occskillpointscenarios(char)
	if mincredit is True:
		lowcredit = refs.rget(refs.occref, char.get("occupation"), "mincredit")
		char["skills"]["Credit Rating"] = {"value": lowcredit, "checked": False}
		skillpoints -= lowcredit
	if invalidoccskill(char, choices, skillpoints):
		raise ValueError("Choices are invalid. Ensure choices are in proper order.")
	return selectskills(char, char.get("skills"), skillpoints, choices, maxskillval, transferable)

def setskills(char, choices={}, maxskillval=99, transferable=False, mincredit=True):

	occskillchoices, piskillchoices = choices.get("occupation"), choices.get("personal")
	return {**char, **{"skills": {**char.get("skills"), **initskills(char), **setstatbasedskills(char), 
				**selectoccskills(char, occskillchoices, mincredit=mincredit, transferable=transferable), 
				**selectskills(char, char.get("skills"), char.get("int") * 2, choices=piskillchoices)}}}
#### Set: Credit Rating, Brawling, Own Language and Dodge ###
#### These values are necessary in order to ensure maxskillval is not exceeded.

#### 5. After skills are set. Needs characters "Credit Rating"
def wealthset(char, ref=genref.get("wealthset")):
	refval = [v for k, v in ref.items() if getskill(char, "Credit Rating")]
	return None

#### Generates a Character without skills.  ####
def chargen(**kwargs):
	char = withrolledchars()
	for k, v in kwargs.items():
		if k in character_template().keys():
			char[k] = v
	for fn, args in kwargs.get("passthru", {}).items():
		char = fn(char, **args)

	char = secondarychars(improvement_check(char))

	char["occupation"] = setoccupation(char)
	return char


def ppfields(_dict, *fields):
	pprint({k:v for k, v in _dict.items() if k in fields})

SECONDARY = ["mov", "db", "build", "hp", "luck"
        "hp", "mp", "sanity", "max_sanity", "dodge"]

if __name__ == "__main__":
	skills = {setskills: {"Brawl":30, "Farming": 40}}
	### fix this:
	# with open("george.json", "r") as fp:
	# 	inv = json.load(fp)
	# passthru = {
	# 	#setskills: {"Brawl":30, "Farming": 40},
	# 	teenage_development: {"changes": {"str": 0, "siz": 0}},
	# 	outofprime_adj: {"changes": {"str": 5, "con": 4, "dex": 1}}}
	# inv = chargen(name="George", occupation="Spy", age=53, passthru=passthru)
	# occskillpoints = occskillpointscenarios(inv) - refs.occref.get("Spy").get("mincredit")
	# piskillpoints = inv.get("int") * 2
	#print(occskillpoints, piskillpoints)
	# skchoices = {
	# 	"occupation": [
	# 		{"name": "Disguise", "value": 30},
	# 		{"name": "Intimidate", "value": 30},
	# 		{"name": "Russian", "value": 50},
	# 		{"name": "Listen", "value": 40},
	# 		{"name": "Psychology", "value": 40},
	# 		{"name": "Stealth", "value": 24}
	# 	],
	# 	"personal": [
	# 		{"name": "Sleight of Hand", "value": 30},
	# 		{"name": "Handgun", "value": 40},
	# 		{"name": "Charm", "value": 30},
	# 		{"name": "French", "value": 34}
	# 	]
	# }
	# inv = setskills(inv, choices=skchoices)
	# pprint(inv)

	# with open("george.json", "w") as fp:
	# 	json.dump(inv, fp)
	#pprint(initskills(inv))
	
		




# def tweakref(data, path):
# 	moreref_genref = {
# 		improvement_check: {"key": "edu", "count": 0}, 
# 		outofprime_adj: {"changes": {"str": 2, "con": 4}}}







