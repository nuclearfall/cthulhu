
import json
import random
from functools import reduce
from pprint import pprint
import occupations as occ
#from anytree import AnyNode



with open("../data/skills.json", "r") as fp:
    skill_defs = json.load(fp)

_SKILL_TEMPLATE = {
	        "name": "Accounting",
	        "pdfslot": "Skill_Accounting",
	        "value": 5,
	        "era": 0,
	        "rarity": "",
	        "notes": "",
	        "description"
	        "custom": False,
	        "checked": False,
	        "children": [],
	        "parent": None,
	        "groups": [],
	        }

def ofera(skill_list, era=0):
	return [s for s in skill_list if skill_defs.get(s).get('era') == era]

def exclude_era(skill_list, era=0):
	return [s for s in skill_list if skill_defs.get(s).get('era') != era]
def get_slots():
	return {
		"ArtCraft": ["1", "2"],
		"Fighting": ["1", "2"], # Brawling is not a defined skill
		"Firearms": [""],
		"OtherLanguage": ["", "1", "2"],
		"Pilot": [""],
		"Science": ["1", "2", "3"],
		"Survival":  [""],
		"Custom": ["1", "2", "3", "4"]
		}

ERAS = ["All", "Modern", "Lovecraftian"]

def exclude_from(_list, exclude=[]):
	return [s for s in skill_list if s not in exclude]
def kv_pair(name, skills=skill_defs):
	for k, v in skill_defs.items():
		if k.get("name") == name:
			return (k, v)
	return None

def is_child(name=None, skill=None):
	if isinstance(name, str):
		return True if find(name=name) is not None else False
	else:
		return True if skill.get("parent") else False

def is_parent(skill, skills=skill_defs):
	if isinstance(skill, str):
		return True if skill_defs.get(skill) and skill_defs.get(skill).get("children") is not None else False
	else:
		return True if skill.get("children") else False

def is_uncommon(skill, skills=skill_defs):
	return True if skill.get("rarity") == "Uncommon" else False

def modernlist(skill_list, skills=skill_defs):
	for skill in skill_list:
		if isinstance(skill, str):
			skill = skills.get(skill)
	return [s for s in skills if s.get("era") != 1]

def inera(skill, era, skills=skill_defs):
	if isinstance(skill, str):
		skill = skills.get(skill)
	return True if skill.get("era") == era else False

def is_member(skill, group):
	return True if group in skill.get("groups") else False

def _lookup(key=None, val=None, skills=skill_defs):
	if key and val:
		return [sk for sk in skills if skills.get(sk).get(key) == val]

def members(group, results=[]):
	for val in skill_defs.values():
		if group in val.get("groups"):
			results.append(val.get("name"))
	return results

def get_skillset(result=[]):
	return [(v.get("name"), v.get("value")) for v in skill_defs.values()]
def _firearms():
	return _lookup(key="parent", val="Firearms")

def _fighting():
	return _lookup(key="parent", val="Fighting")

def _science():
	return _lookup(key="parent", val="Science")

def _language():
	return _lookup(key="parent", val="Other Language")

def _survival():
	return _lookup(key="parent", val="Survival")

def _science():
	return _lookup(key="parent", val="Science")

def _interpersonal():
	return _lookup(key="group", val="interpersonal")

def names(current_skills=[], skills=skill_defs):
	return [k for k in skills.keys(
			) if k in skills and k not in current_skills]

def children_of(skill=None, skills=skill_defs):
	if isinstance(skill, str):
		return skills.get(name).get("children")
	else:
		return skill.get("children")

def children(skills=skill_defs):
	return [child for parent in parents() for child in children_of(parent)]

def parents(skills=skill_defs):
	return {k:v for k, v in skills.items() if v.get("children")}

def noparents(skills=skill_defs):
	return {k:v for k, v in skills.items() if not v.get("children")}

def orphans(skills=skill_defs):
	return {k:v for k, v in skills.items() if not v.get("parent") and not v.get("children")}

def nochildren(skills=skill_defs):
	return {k:v for k, v in skills.items() if not v.get("parent")}

# def is_member(key=None, group=[], possible=[], item_dict=skill_defs):
# 	for member in possible:
# 		member_exists = item_dict.get(member)
# 		key_group = member_exists.get(key)
# 		if member_exists and key_group:
# 			return member in key_group 
def all_skills(skills=skill_defs):
	return skills

def add_group(group, skill_names=[], skills=skill_defs):
	for name in skill_names:
		is_skill = skills.get(name)
		groups = is_skill.get("groups")
		if group not in groups:
			skills[name]["groups"].append(group)
	return skills

def member_list(group, skills=skill_defs):
	members = []
	for skill in skills.values():
		groups = skill.get("groups")
		if group in groups:
			members.append(skill.get("name"))
	return members

def create_custom(skills=skill_defs, **kwargs):
	pass

def find_all(key=None, val=None, skills=skill_defs):
	matches = []
	if key and val:
		for skill in skills.values():
			skill_value = skill.get(key)
			if skill_value and skill_value == val:
				matches.append(skill)
	else:
		matchs = [skill for skill in skills.values()]
		
def find(key=None, val=None, skills=skill_defs):
	if key:
		for name, skill in skills.items():
			if skill.get(key) and skill.get(key) == val:
				return skill
	return None 

def add_field(key=None, value="", skills=skill_defs):
	for name, skill in skills.items():
		skills[name][key] = value
	return skills

def pdf_lookup(name):
	return find(key="name", val=name).get("pdfslot")

def pdf_skill_fields(skill, str_num=None):
	pdf_template = skill.get("pdfslot")
	pdf_chk = skill.get("")
	if str_num:
		pdf_template = skill.get("pdfslot") + str_num
		pdf_field_name = "SkillDef_" + pdf_template[6:]

def assign_skill(skill, csheet, str_num=None):
	if num:
		slot_name = skill.get("pdfslot") + str_num

def skill_init(name, value=0, keys=["name", "parent", "value", "pdfslot"], skill=skill_defs):
	skill = skills.get("name")
	if skill:
		return {k: v+value for k, v in skill.items() if k in keys}
	# else:
	# 	raise ValueError(f"Skill {name} does not exist.")

# def set_skill(investigator, choice, slotdefs):
# 	skname, value, parent, is_custom = choice
# 	skill = find(key="name", val=skname)
# 	pdfslot = skill.get("pdfslot")
# 	pdfslot = pdfslot[6:]
# 	value += skill.get("value", 0)
# 	pdf_children = [sn for sn in slotdefs]

# 	if skname == "Brawling" or pdfslot not in pdf_children:
# 		csheet[pdfslot] = value 
# 	elif len(slotdefs.get(pdfslot)) == 0 or pdfslot == "Skill_Custom":
# 		pdfnum = slotdefs["Custom"].pop(0)
# 		csheet["SkillDef_Custom"+pdfnum] = skname 
# 		csheet["Skill_Custom"+num] = value
# 	else:
# 		pdfnum = slotdefs[pdfslot].pop(0)
# 		csheet["SkillDef_"+pdfslot+pdfnum] = skname 
# 		csheet["Skill_"+pdfslot+pdfnum] = value

# 	return (csheet, slotdefs)

# def set_min_credit_skill(character, skill_points):
# 	occupation = character.get("Occupation")
# 	min_credit = occ.occ_defs.get("minCredit")
# 	character["Skill_Credit"] = min_credit
# 	skill_points -= min_credit 
# 	return skill_points

# def set_personal_interest_skills(csheet, selection):
# 	slotdefs = get_slots()
# 	for item in selections:
# 		csheet, slotdefs = set_skill(csheet, item, slotdefs)
# 		point_pool -= 
# 	return csheet

# def add_required(skillset:dict):
# 	pdf_children = [sn for sn in get_slots()]
# 	skilllist = [sn for sn in skillset]
# 	return {**skillset, **{sn: skill_init(sn) for sn in pdf_children if sn not in skilllist}}

# def add_edgecase(skillset):
# 	skill_list = [name for name in skillset]
# 	if not "Dodge" in skill_list
# 		skillset = setskill("Dodge", value=int(inv.dex/2))
# 		olang = setskill("Own Language", value=inv.edu)
# 	if not "Brawl" in skill_list
# 		skillset["Brawl"] setskill("Brawl")
# 	return {"Dodge":dodge, "Own Language":olang, "Brawl":brawl}

# def setskill(name, skillset, value=0):
# 	if skillset.get(name):
# 		skills = skillset
# 	return {**skillset, **{name: skill_init(name, value=value, skills=skillset)}}
	
# def get_options(selection, exclude=[]):
# 	group = selection.get("group")
# 	options = selection.get("selections")
# 	if group:
# 		return members(selection.get("group"))
# 	elif options is not None:
# 		options = parent_replace(options)
# 	else:
# 		new_options = []
# 	return new_options

# def parent_replace(options, result=[]):
# 	for option in options:
# 		if is_parent(option):
# 			result += children_of(option)
# 		else:
# 			result.append(option)
# 		return result 

# def add_skill(choices, selection, count=0, exclude=[]):
# 	skills = []
# 	if count == selection.get("count"):
# 		return skill_list
# 	while count < selection.get("count"):
# 		choice = choices.pop(0)
# 		options = options(selection)
# 		if choice not in options:
# 			raise ValueError(f"{choice} is not in selection {options}")
# 		skills.append(choice)
# 		count += 1
# 	return (choices, skills)
			
# # Before this goes check skills to see if edgecase there. If not cehck after first
# # run. If still not, add in final.
# def add_skills(choices, selections=[{"count": 1, "selections": []}], is_occupation=True, 
# 			exclude=[], skills=[]):
# 	index = 0
# 	while choices:
# 		selection = selections[index]
# 		choices, new_skills = add_skill(choices, selection)
# 		skills += new_skills
# 		index += 1
# 	return {sn:skill_init(sn) for sn in skills}

# def allocate_skillpoints(skillpoints, allocations, skillset, max_skill=99):
# 	#skillset = add_edgecases(skillset)
# 	for akey, adict in allocations.items():
# 		if skillpoints = 0:
# 			return skillset
# 		aval = adict.get("value")
# 		if skillpoints - val < 0:
# 			raise ValueError(f"Allocation to {adict.get('name')} would result in negative skill points: {skillpoints-val}")
# 		if value + aval <= max_skill:
# 			skillset[akey] = set_skill(akey, value=value+aval, skilset=skillset)
# 			skillpoints = skillpoints - aval
# 		else:
# 			raise ValueError(f"Skill cannot exceed a value of {max_skill}.")
# 	return (skillpoints, skillset)


class Skills:
	def __init__(skill_defs=skill_defs, era=0):
		defs = skill_defs
		for key, data in skill_defs.items():
			if data.get('era') == era:
				setattr(key.replace(" ", "_").replace("/", "_"), Skill(data))

	def find(key="name"):
		return getattr(key)

	def get_names(key=None, val=None):
		if not key and not val:
			return 

	def pdfset_skill(investigator, choice, slotdefs):
		skname, value = choice
		skill = find(key="name", val=skname)
		pdfslot = skill.get("pdfslot")
		pdfslot = pdfslot
		value += skill.get("value", 0)
		pdf_children = [sn for sn in slotdefs]

		if skname == "Brawling" or pdfslot not in pdf_children:
			investigator.pdf["Skill_"+pdfslot] = value 
		elif len(slotdefs.get(pdfslot)) == 0 or pdfslot == "Skill_Custom":
			pdfnum = slotdefs["Custom"].pop(0)
			investigator.pdf["SkillDef_Custom"+pdfnum] = skname
			investigator.pdf["Skill_Custom"+num] = value
		else:
			pdfnum = slotdefs[pdfslot].pop(0)
			investigator.pdf["SkillDef_"+pdfslot+pdfnum] = skname 
			investigator.pdf["Skill_"+pdfslot+pdfnum] = value

		return (value, slotdefs)


# class Skill:
# 	def __init__(skill_def):
# 		for key, data in skill_def.items():
# 			if _SKILL_TEMPLATE.get(key):
# 				setattr(key, data)

# 	def is_child():
# 		return True if parent else False

# 	def is_parent():
# 		return True if children else False

# 	def is_modern():
# 		return True if era == 1 else False

# 	def is_member(group):
# 		return True if group in groups else False

# 	def pdf_export(numstr="", points=0, result={}):
# 		value += points
# 		pdfname = f"Skill_{pdfslot}{numstr}"
# 		if get_slots().get(pdfslot):
# 			result[f"SkillDef_{pdfslot}"] = name
# 		result[f"{pdfname}"] = value
# 		return result

if __name__ == "__main__":
	skills = Skills(skill_defs)
	print(skills.Brawl.pdf_export(points=20))



