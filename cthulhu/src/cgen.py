import json
import random
import fillpdf
from pprint import pprint
from fillpdf import fillpdfs
import skills as skl
import occupations as occ
import character
from functools import reduce
from pathlib import Path
import pickle
random.seed()

_primary = ["pow", "str", "con", "dex", "app", "siz", "edu", "int"]

with open("../data/investigator.json") as fp:
	template = json.load(fp)
with open("../data/character.json") as fp:
	char_refs = json.load(fp)	
with open("../data/reference.json") as fp:
	create_refs = json.load(fp)
with open("../data/occupations.json") as fp:
	occ_refs = json.load(fp)
with open("../data/skills.json") as fp:
	skill_refs = json.load(fp)



def validate_input(data, typeof=[dict, tuple, list], fn=None, error=""):
	try:
		if type(data) in typeof:
			return fn(data) if fn else data
	except:
		raise ValueError(error)


class InvestigatorGen:
	def __init__(self, name, age, occupation="", language="English",
				age_adjustment=None, occ_skill_choices=[], era=0,
				presets=None, pdf=None, **kwargs):
		self.era = era
		self.name = name
		self.age = age or random.randrange(18, 54)
		self.occname = occupation
		self.language = language
		self.skills = {}
		self.investigator = character.Investigator(name=self.name, age=self.age, 
				occupation=occupation, language=language, **kwargs)
		if presets:
			for key, preval in presets.items():
				if key in template.values():
					setattr(self.investigator, key, preval)
		else:
			self.rollchars()
		setattr(self.investigator, "mov", self.set_move_rate())
		self.set_age_reference()
		if age_adjustment or age in range(20,40):
			self.age_adjust(age_adjustment)
		else:
			raise ValueError(f"Character requires age penalties in key, val pairs (eg. ('dex', 3) ('str', 2)': {self.penalties}")

		self.set_secondary_chars()
		self.occupation = occ.Occupation(self, self.occname)
		self.age_adjusted = True
		self.occ_skillpoints = self.occupation.skillpoints
		self.pi_skillpoints = self.investigator.int * 2

	def invsetattrs(self, kv_pairs):
		[setattr(self.investigator, k, v) for k, v in kv_pairs.items()]

	def rollchars(self, d6=3, mul=5, add=0):
		#rollrange = random.randrange(int(d6/1), d6*6+1)
		chark3d6 = ['str', 'con', 'dex', 'app', 'pow', 'luck']
		chark2d6 = ['siz', 'edu', 'int']
		charv3d6 = [random.randrange(3,19)*5 for i in range(0, len(chark3d6))]
		charv2d6 = [(random.randrange(2,13)+6)*5 for i in range(0, len(chark2d6))]
		chars = dict(zip(chark3d6 + chark2d6, charv3d6 + charv2d6))
		self.invsetattrs(chars)

	def getchars(self):
		return {k:val for k in _PRIMARY_CHARS for key, val in self.investigator.__dict__.items() if k == key}

	def set_secondary_chars(self):
		db, build = self.db_and_build(self.investigator.siz+self.investigator.str)
		# These skills need to be set to ensure that they can be assigned for occupations.
		# self.skills["Dodge"] = int(self.investigator.dex / 2)
		# self.skills["Own Language"] = self.investigator.edu
		chars = {
				"db": db, 
				"build": build,
				"hp": int((self.investigator.con + self.investigator.con) / 10),
				"mp": int(self.investigator.pow / 5),
				"sanity": self.investigator.pow,
				"max_sanity": 99,
				"mov": self.set_move_rate()
			}
		self.invsetattrs(chars)

	def db_and_build(self, str_siz):
	    for comp in create_refs.get("Build_and_Db"):
	        if comp.get("lowValue") <= str_siz <= comp.get("highValue"):
	            return (comp.get("DamageBonus"), comp.get("Build"))
	    raise ValueError("Build and Damage Bonus couldn't be set")

	def set_age_reference(self): 
		for key, agemods in create_refs.get("age_modifiers").items():
			if agemods.get("ageLow") <= self.age < agemods.get("ageHigh"):
				self.penalties = agemods.get("penalties")
				self.educhecks = agemods.get("edu_checks")
				return None
		raise ValueError("Age out of range.")

	def set_wealth(self, wealth_key=""):
		credit = self.skills.get("Credit Rating").get("value")
		wealth_ref = create_refs.get("Wealth")
		wealthrng = [list(map(int, w.split("-"))) for w in wealth_ref]
		for w in wealth_ref:
			wlow, whigh = list(map(int, w.split("-")))
			if wlow <= credit < whigh:
				wealth_key = w
		wealth_ref = wealth_ref.get(w)
		cashmult = wealth_ref.get("CashMult")
		if cashmult:
			self.investigator.assets = wealth_ref.get("AssetMult") * credit
			self.investigator.cash = cashmult * credit
		else:
			self.investigator.cash = wealth_ref.get("Cash")
			self.investigator.assets = wealth_ref.get("Assets")
		spending = wealth_ref.get("SpendingLevel")
		wealth = wealth_ref.get("name")
		self.investigator.spending_level = f"{spending} ({wealth})"


	def age_adjust(self, choices=(), age=20):
		if choices:
			choices = validate_input_type(choices, (dict, tuple, list), 
					"Invalid type for selection.")
		total = 0
		while choices:
			choices = list(choices)
			key, pen = choices.pop()
			self.penchars(key, pen)
			total += abs(pen)
		if total != abs(sum([p[0] for p in self.penalties if len(p) > 2])):
			raise ValueError("Penalty value does not equal required total.")
		if self.educhecks:
			self.investigator.improvement_check("edu", self.educhecks)
		return None

	def penchars(self, key, penalty):
		val = getattr(self.investigator, key)
		setattr(self.investigator, key, val-abs(penalty))

	def set_move_rate(self):
		inv = self.investigator
		if inv.str > inv.siz and inv.dex > inv.siz:
			self.investigator.mov = 9
		elif inv.str > inv.siz or inv.dex > inv.siz or (inv.dex == inv.siz == inv.str):
			self.investigator.mov = 8
		else:
			self.investigator.mov = 7

	def init_skill(self, key:str, value=0, keys=["name", "parent", "value", "pdfslot", "checked"]):
		if key in self.skills:
			self.skills[key]["value"] += value
		else:
			self.skills[key] = {k:v for k, v in skill_refs.get(key).items() if k in keys}
			self.skills[key]["value"] += value


	# Check for malformed data here:
	def set_skills(self, choices=None):
		if not choices:
			return f"{self.occ_skillpoints} occupation skill points and {self.pi_skillpoints} personal interest skillpoints remain to assign."
		occ_choices, pi_choices = (choices.get("Occupation"), choices.get("Personal Interest"))
		if not self.skills:
			min_credit = occ_refs.get(self.occname).get("mincredit")
			self.init_skill("Credit Rating", value=int(min_credit))
		# if len(self.occupation.skills) != list(filter(lambda x: x in self.skills, self.occupation.skills)):
			for key in self.skills:
				self.init_skill(key)
		if occ_choices:
			self.occ_skillpoints = self.from_selections(occ_choices, "occ_skillpoints", self.occupation.selections)
			
			if self.occ_skillpoints > 0:
				return f"{self.occ_skillpoints} occupation skillpoints remain to assign"
		if pi_choices:
			pi_selections = [{"count": 99, "selections": []}]
			self.pi_skillpoints = self.from_selections(pi_choices, "pi_skillpoints", pi_selections)
			if self.occ_skillpoints > 0:
				return f"{self.pi_skillpoints} personal interest skillpoints remain to assign."
		if self.pi_skillpoints == self.occ_skillpoints == 0:
			[self.init_skill(k) for k, v in skill_refs.items() if v.get("pdfslot") and v.get(
					"pdfslot") not in skl.get_slots() and k not in self.skills and v.get("era") == 0]
			self.edgecases()
			self.investigator.dodge = self.skills.get("Dodge")
			self.investigator.skills = self.skills
			self.set_wealth()
		return None 

	def edgecases(self):
		dkey, dval, okey, oval = ("Dodge", int(self.investigator.dex/2), "Own Language", self.investigator.edu)
		#if (okey in self.skills and step == 0) or (okey not in self.skills and step == 1):
		self.init_skill("Own Language", value=oval)
		#if (dkey in self.skills and step == 0) or (dkey not in self.skills and step == 1):
		self.init_skill("Dodge", value=dval)

	def from_selections(self, choices:list, pool:str, selections=None, options=False,
			exclude=[], skill_list=[], count= 0, index=0):
		print("Pool before assignment")
		pool = getattr(self, pool)

		### TODO: Fix faulty logic in selection validation.
		for key, points in choices.items():
			# self.init_skill(key, value=points)
			# pool -= points
		#############
			# if selections[index].get("count") == count:
			# 	count, index = (0, index+1)
			# 	if index 
			# 	print(count, index)
			# if options == False or choice in get_options(selection[index]):
			pool -= self.valid_assignment(key, points, pool)
			# 	count += 1
		#############	
		return pool

	def valid_assignment(self, key, points, pool, max_skill=99):
		if key in self.skills:
			val = self.skills.get(key).get("value")
		else:
			val = skill_refs.get(key).get("value")
		if val + points < max_skill and pool - points >= 0:
			self.init_skill(key, value=points)
			print(f"Pool after assignment to {key}")
			return points
		else:
			raise ValueError(f"assignment to {key} exceeds {max_skill} or points assigned reduces pool to {pool-points}")


	def get_options(self, selection, exclude=[]):
		group = selection.get("group")
		options = selection.get("selections")
		if group:
			return members(selection.get("group"))
		elif options == []:
			return [s for s in skill_refs if not skill_refs.get(s).get("children")]
		elif options:
			new_options = replace_option_parents(options)
		return new_options

	def replace_option_parents(self, options, result=[]):
		for option in options:
			if skl.is_parent(option):
				result += [c for c in skill_refs.vals() if c.get("parent") == option]
			else:
				result.append(option)
			return result 



def gendump(investigator, path):
    path = Path(path)
    if not path.exists():
        path.touch()
    path.write_bytes(pickle.dumps(investigator))

def genload(path):
    path = Path(path)
    if path.exists():
        return pickle.loads(path.read_bytes())










