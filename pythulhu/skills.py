
import json
import random
from functools import reduce
from pprint import pprint
from refs import skillref, rget, attrget, rgetlist

#import occupations as occ



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


def fromera(skill_list, era=0):
	return [s for s in skill_list if skillref.get(s).get('era') == era]

def exclude_era(skill_list, era=0):
	return [s for s in skill_list if skillref.get(s).get('era') != era]
def getslots():
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
def kv_pair(name, skills=skillref):
	for k, v in skillref.items():
		if k.get("name") == name:
			return (k, v)
	return None
def groups():
	return ["languages", "science", "firearms", "artcraft", "fighting", 
				"survival", "pilot", "interpersonal"]
def is_child(name=None, skill=None):
	if isinstance(name, str):
		return True if find(name=name) is not None else False
	else:
		return True if skill.get("parent") else False

def is_parent(skill, skills=skillref):
	if isinstance(skill, str):
		return True if skillref.get(skill) and skillref.get(skill).get("children") is not None else False
	else:
		return True if skill.get("children") else False

def is_uncommon(skill, skills=skillref):
	return True if skill.get("rarity") == "Uncommon" else False

def modernlist(skill_list, skills=skillref):
	for skill in skill_list:
		if isinstance(skill, str):
			skill = skills.get(skill)
	return [s for s in skills if s.get("era") != 1]

def inera(skill, era, skills=skillref):
	if isinstance(skill, str):
		skill = skills.get(skill)
	return True if skill.get("era") == era else False

def is_group(name):
	return True if name in self.groups else False

def is_member(skill, group):
	return True if group in skill.get("groups") else False

def _lookup(key=None, val=None, skills=skillref):
	if key and val:
		return [sk for sk in skills if skills.get(sk).get(key) == val]

def members(group, results=[]):
	for val in skillref.values():
		if group in val.get("groups"):
			results.append(val.get("name"))
	return results

def get_skillset(result=[]):
	return [(v.get("name"), v.get("value")) for v in skillref.values()]
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

def names(current_skills=[], skills=skillref):
	return [k for k in skills.keys(
			) if k in skills and k not in current_skills]

def children_of(skill=None, skills=skillref):
	if isinstance(skill, str):
		return skills.get(name).get("children")
	else:
		return skill.get("children")

def groupies(group=None, skills=skillref, ret_type=dict):
		# if a specific
	groups = {k:v, for k, v in skills.items() if v.get("group")}
	if skill is None and ret_type == dict:
		return parents
	if skill is None and ret_type == list or ret_type == tuple:
		return ret_type([v for v in parents.values()])
	if skill and ret_type == dict:
		return {k:v for k, v in parents.items() if v.get("parent") == skill}
	if skill and ret_type == list or ret_type == tuple:
		return ret_type([v for k, v in skills.values(), if v.get("parent") == skill])

def children(parent:str, skills=skillref, ret_type:dict):
	# if a specific
	parents = {k:v, for k, v in skills.items() if v.get("parent")}
	if parent is None and ret_type == dict:
		return parents
	if parent is None and ret_type == list or ret_type == tuple:
		return ret_type([v for v in parents.values()])
	if parent and ret_type == dict:
		return {k:v for k, v in parents.items() if v.get("parent") == parent}
	if parent and ret_type == list or ret_type == tuple:
		return ret_type([v for k, v in skills.values(), if v.get("parent") == parent])


def parents(skills=skillref):
	return {k:v for k, v in skills.items() if v.get("children")}

def noparents(skills=skillref):
	return {k:v for k, v in skills.items() if not v.get("children")}

def orphans(skills=skillref):
	return {k:v for k, v in skills.items() if not v.get("parent") and not v.get("children")}

def nochildren(skills=skillref, in_dict=False):
	return {k:v for k, v in skills.items() if not v.get("parent")}

# def is_member(key=None, group=[], possible=[], item_dict=skillref):
# 	for member in possible:
# 		member_exists = item_dict.get(member)
# 		key_group = member_exists.get(key)
# 		if member_exists and key_group:
# 			return member in key_group 
def all_skills(skills=skillref):
	return skills

def add_group(group, skill_names=[], skills=skillref):
	for name in skill_names:
		is_skill = skills.get(name)
		groups = is_skill.get("groups")
		if group not in groups:
			skills[name]["groups"].append(group)
	return skills

def member_list(group, skills=skillref):
	members = []
	for skill in skills.values():
		groups = skill.get("groups")
		if group in groups:
			members.append(skill.get("name"))
	return members

def create_custom(skills=skillref, **kwargs):
	pass

def find_all(key=None, val=None, skills=skillref):
	matches = []
	if key and val:
		for skill in skills.values():
			skill_value = skill.get(key)
			if skill_value and skill_value == val:
				matches.append(skill)
	else:
		matchs = [skill for skill in skills.values()]
		
def find(key=None, val=None, skills=skillref):
	if key:
		for name, skill in skills.items():
			if skill.get(key) and skill.get(key) == val:
				return skill
	return None 


def add_field(key=None, value="", skills=skillref):
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

def skill_init(name, value=0, keys=["name", "parent", "value", "pdfslot"], skill=skillref):
	skill = skills.get("name")
	if skill:
		return {k: v+value for k, v in skill.items() if k in keys}


class SkillGroup:
	def __init__(self, name, skills=skillref, era=0, issubgroup=False):
		self.skills = {}
		self.groups = groups()

		for key, val in skills.items():
			children, groups, parent = rgetlist(val, "children", "groups", "parent")
			if issubgroup is False and groups:
				groupobj = SkillGroup(group, skills=members(group), era=era, issubgroup=True)
				try:
					getattr(group)
				setattr(self, group, groupobj)
				# all other grouped are specialties and should be saved under their parent group.
				if "interpersonal" in group:
					self.skills[k] = v
			if children and not issubgroup:
				groupobj = SkillGroup(group, skills=children(k), era=era, issubgroup=True)
				setattr(self, sanitize_key(k), groupobj)
			if parent:
				pass
			else:
				setattr(self, sanitize_key(k), val)
		self.name = name
	def find(self, key):
		return self.skills.get(key)
	def list(self, selectable=True):
		return [v for v in self.skills.values()]
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

class Skill:
	def __init__(self, group:SkillGroup, name:str, data:dict):
		self.group = group
		self.name = name
		for key, val in data.items():
			setattr(self, sanitize_key(key), val)
	def roll_against(self):
		pass


if __name__ == "__main__":
	skills = Skills(skillref)
	print(skills.Brawl.pdf_export(points=20))



