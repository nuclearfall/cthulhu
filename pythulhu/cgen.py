import json
import random
import fillpdf
import refs
from pprint import pprint
from fillpdf import fillpdfs
import .skills as skl
import .occupations as occ
import .character.character
from .occupations import Occupation
from .skills import is_group, members, getslots
from .refs import genref, occref, skillref, topdftemp, svalget
from functools import reduce
from pathlib import Path
random.seed()

_primary = ["pow", "str", "con", "dex", "app", "siz", "edu", "int"]


def validate_input(data, typeof=[dict, tuple, list], fn=None, error=""):
	try:
		if type(data) in typeof:
			return fn(data) if fn else data
	except:
		raise ValueError(error)

class CharacterGen:
	def __init__(self, name, occupation="", language="English",
				age_adjustment=None, occ_skill_choices=[], era=0,
				presets=None, pdf=None, **kwargs):
		self.is_age_adjusted = False
		self.era = era
		self.name = name
		self.age = kwargs.get("age", None)
		self.occname = occupation
		self.language = language
		self.skills = {}
		if presets:
			for key, preval in presets.items():
				if key in topdftemp.values():
					setattr(self.character, key, preval)
					self.age_adjusted = True

	def approve(self, method, appflag=True, step=0):
		step_method = self.mget(step)

	def invsetattrs(self, kv_pairs):
		[setattr(self.character, k, v) for k, v in kv_pairs.items()]

	def rollchars(self, d6=3, mul=5, add=0):
		chark3d6 = ['str', 'con', 'dex', 'app', 'pow', 'luck']
		chark2d6 = ['siz', 'edu', 'int']
		charv3d6 = [random.randrange(3,19)*5 for i in range(0, len(chark3d6))]
		charv2d6 = [(random.randrange(2,13)+6)*5 for i in range(0, len(chark2d6))]
		self.chars = dict(zip(chark3d6 + chark2d6, charv3d6 + charv2d6))
		return self.chars

	def set_secondary_chars(self):
		db, build = self.db_and_build(self.character.siz+self.character.str)
		chars = {
				"db": db, 
				"build": build,
				"hp": int((self.character.con + self.character.con) / 10),
				"mp": int(self.character.pow / 5),
				"sanity": self.character.pow,
				"max_sanity": 99,
				"mov": self.set_move_rate()
			}
		self.invsetattrs(chars)
		return 2

	def db_and_build(self, str_siz):
	    for comp in genref.get("Build_and_Db"):
	        if comp.get("lowValue") <= str_siz <= comp.get("highValue"):
	            return (comp.get("DamageBonus"), comp.get("Build"))
	    raise ValueError("Build and Damage Bonus couldn't be set")

	def set_age_reference(self): 
		for key, agemods in genref.get("age_modifiers").items():
			if agemods.get("ageLow") <= self.age < agemods.get("ageHigh"):
				self.penalties = agemods.get("penalties")
				self.educhecks = agemods.get("edu_checks", 0)
		return None

	def set_wealth(self, wealth_key=""):
		credit = svalget(self, "Credit Rating")
		wealth_ref = genref.get("Wealth")
		wealthrng = [list(map(int, w.split("-"))) for w in wealth_ref]
		for w in wealth_ref:
			wlow, whigh = list(map(int, w.split("-")))
			if wlow == 0:
				wealth_key = w
			elif wlow <= credit < whigh:
				wealth_key = w
		wealth_ref = wealth_ref.get(wealth_key)
		cashmult = wealth_ref.get("CashMult")
		if cashmult:
			self.character.assets = wealth_ref.get("AssetMult") * credit
			self.character.cash = cashmult * credit
		else:
			self.character.cash = wealth_ref.get("Cash")
			self.character.assets = wealth_ref.get("Assets")
		spending = wealth_ref.get("SpendingLevel")
		wealth = wealth_ref.get("name")
		self.character.spending_level = f"{spending} ({wealth})"

	# weighted random distribution. Majority of character should fall between 20-40, some in 
	def random_age(self):
		age_range = random.choices(population=[random.randrange(15,20), random.randrange(20,40), 
							random.randrange(40,50), random.randrange(50,60), random.randrange(60,80)], 
							k=1, weights=[0.02, 0.65, 0.2, 0.1, 0.05])
		return age_range[0]

	def age_adjust(self, choices=None, age=20, random_age=False):
		self.set_age_reference()
		if random_age is True:
			self.set_age_reference()
			selection = self.penalties
			decisions = []
			for penalty in selection:
				if len(penalty) > 2:
					points, *stats = penalty
					distro = self.constrained_pos_sum(len(stats), abs(points))
					choices = list(zip(stats, distro))
		elif choices:
			self.set_age_reference()
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

		self.character.improvement_check("edu")
		return True

	def penchars(self, key, penalty):
		val = getattr(self.character, key)
		setattr(self.character, key, val-abs(penalty))

	def set_move_rate(self):
		inv = self.character
		if inv.str > inv.siz and inv.dex > inv.siz:
			self.character.mov = 9
		elif inv.str > inv.siz or inv.dex > inv.siz or (inv.dex == inv.siz == inv.str):
			self.character.mov = 8
		else:
			self.character.mov = 7
		return True

# ensure player has submitted all necessary decisions or decided 
	# on random_skills decision making for choices:
	def set_skillpoints(self, best=0):
		chars = self.chars
		for scenario in self.selections:
			total = 0
			for key, val in scenario.items():
				total += chars.get(key) * val
				if total > best:
					best = total
		return best

	def generate_random(self, **kwargs):
		self.selections = rget(occref, self.occname, "selections")
		self.character = character.Investigator(name=self.name 
				occupation=self.occname, language=kwargs.get("language"), **kwargs)
		self.language = kwargs.get("language", "English")
		chars = self.rollchars()
		for char, roll in chars.items():
			setattr(self.character, char, roll)	
		self.occupation = Occupation(self, self.occname)		
		self.age = self.random_age()
		self.set_age_reference()
		self.age_adjust()
		self.is_age_adjusted = True
		self.set_secondary_chars()
		self.occ_skillpoints = self.set_skillpoints()
		self.pi_skillpoints = self.character.int * 2
		self.set_occ(occname, mincredit=kwargs.get("mincredit", True))
		self.random_set_skills()
		self.character.skills = self.skills
		self.set_wealth()
		self.character.dodge = self.skills.get("Dodge")
		return self.character


	def generate(self, **kwargs):
		if kwargs.get("random_age"):
			return self.generate_random()
		self.language = kwargs.get("language", "English")
		self.character = character.Investigator(name=self.name, age=self.age, 
				occupation=self.occname, language=kwargs.get("language"), **kwargs)
		self.rollchars()
		self.age = kwargs.get("age", self.age)
		self.age_adjust(kwargs.get("age_adjustments"))
		self.set_secondary_chars()
		# set occupation, occ_skillpoints
		self.occ_set(kwargs.get("occupation"))
		self.pi_skillpoints = self.character.int * 2
		# allow players to revisit with skill selections.
		if kwargs.get("skill_selection", None) or kwargs.get("random_skills"):
			# skill selection should either be a dict of skill:value pairs or
			# "random_skills=True
			self.occ_skillpoints = self.set_skillpoints()
			self.set_skills(choices=kwargs.get("skill_selections", None))
			self.set_wealth()
			self.character.skills = self.skills
			self.character.dodge = self.skills.get("Dodge")
			return self.character
		else:
			return None

	def set_occ(self, occname=None, mincredit=True, custom=False):
		if occref.get(occname):
			self.occname = occname
		else:
			self.occname = random.choice([occ for occ in occref])
			occmin = 0
		if mincredit:
			occmin = rget(occref, occname, "mincredit")
		self.occupation = Occupation(self, kwargs.get("occupation"))
		self.occ_skillpoints -= occmin
		self.init_skill("Credit Rating", value=occmin)
		return 

	def set_skillpoints(self, occname, total=0, best=0):
		chars = self.character.getchars()
		for scenario in rget(occref, occname, "scenarios"):
			for key, val in scenario.items():
				total += self.character.getchars(). * val
				best = total if total > best else best
		return best

	def init_skill(self, key:str, value=0, pdfslot=None, max_skill=99,
				keys=["name", "parent", "value", "pdfslot", "checked", "custom"]):
		if not key in self.skills:
			self.skills[key] = skillref[key]
		start_val = self.skills.get("value", 0)
		if value + start_val > max_skill:
			raise ValueError(f"Assignment exceed maximum for {key}: {value} and {start_val}")
		self.skills[key]["value"] += value
		return self.skills

	def expand_choices(self, selection, acc=[], index=0):
		if index == len(selection) - 1:
			return acc 
		elif is_group(selection[index]):
			acc += members(selection[index])
			self.expand_choices(selection, acc, index+1)
		else:
			acc.append(selection[index])
			self.expand_choices(selection, acc, index+1)

	def sample(self, total, constraints):
		import numpy as np
		constraints = np.array(constraints)
		rng = np.random.default_rng()
		samples = rng.multinomial(total, constraints / constraints.sum(), size=1).tolist()
		return samples[0]
		#(val for val in samples if np.all(val.any() < constraints.all()))

	def constrained_pos_sum(self, n, total):
		constraints = [random.randrange(20, 50) for i in range(n)]
		samples = self.sample(total, constraints)
		return samples

	def skills_from_selections(self, choices=[], selections=None, has_groups=True):
		skillref = getref("skills")
		for selection in selections:
			if selection == ["any"]:
				any_skill = [skill for skill in skillref.keys() if skill not in choices]
				choices.append(random.choice(any_skill))
			elif has_groups() is True:
				choices.append(random.choice(self.expand_choices(selection, choices)))
			if random is True:
				choices.append(random.choice([s for s in skill_choices if s not in choices]))
		return choices

	def random_set_skills(self):
		skills = {} 
		occ_skills = self.skills_from_selections(selections=self.selections) + refs.jsonref("occref").get(self.occname).get("skills")
		rand_occ_assign = self.constrained_pos_sum(8, self.occ_skillpoints)
		occs = list(zip(occ_skills, rand_occ_assign))
		occ_assigns = {"Occupation": dict(tuple(zip(occ_skills, rand_occ_assign)))}
		pi_selections = [["any"] for i in range(8)]
		#pi_selections = self.skills_from_selections().get("Personal Interest")
		pi_skills = self.skills_from_selections(selections=pi_selections)
		rand_pi_assign = self.constrained_pos_sum(8, self.pi_skillpoints)
		pi_assigns = {"Personal Interest": dict(tuple(zip(pi_skills, rand_pi_assign)))}
		for key, value in occ_assigns.get("Occupation").items():
			self.init_skill(key, value)
		for key, value in pi_assigns.get("Personal Interest").items():
			self.init_skill(key, value)
		return True

	# Check for malformed data here:
	def set_skills(self, choices):
		occ_choices = choices.get("Occupation")
		pi_choices = choices.get("Personal Interest")
		if not choices:
			return f"{self.occ_skillpoints} occupation skill points and {self.pi_skillpoints} personal interest skillpoints remain to assign."
		if not self.skills:
			for key in self.skills:
			[self.init_skill(key) for key in occref.get("skills")
		# Step through and wait for all skill decisions to be made before moving on.
		if occ_choices:
			self.occ_skills = self.from_selections(occ_choices, "occ_skillpoints")
			if self.occ_skillpoints > 0:
				return f"{self.occ_skillpoints} occupation skillpoints remain to assign"
		if pi_choices:
			pi_selections = [{"count": 99, "selections": []}]
			if self.occ_skillpoints > 0:
				return f"{self.pi_skillpoints} personal interest skillpoints remain to assign."
		if self.pi_skillpoints == self.occ_skillpoints == 0:
			[self.init_skill(k) for k, v in skillref.items() if v.get("pdfslot") and v.get(
					"pdfslot") not in getslots() and k not in self.skills and v.get("era") == 0]
			self.edgecases()
			return True
		return None

	def edgecases(self):
		dkey, dval, okey, oval = ("Dodge", int(self.character.dex/2), "Own Language", self.character.edu)
		#if (okey in self.skills and step == 0) or (okey not in self.skills and step == 1):
		self.init_skill("Own Language", value=oval)
		#if (dkey in self.skills and step == 0) or (dkey not in self.skills and step == 1):
		self.init_skill("Dodge", value=dval)

	def valid_assignment(self, key, val, pool, max_skill=99):

		if val + points < max_skill and pool - points >= 0:
			self.init_skill(key, value=points)
			return points
		else:
			raise ValueError(f"assignment to {key} exceeds {max_skill} or points assigned reduces pool to {pool-points}")

	# selection index and group(if any) are required. If skill is selected from presets, index = -1
	# 
	def from_selections(self, choices:dict, pool:int, max_skill=99):
		pool = getattr(self, pool)
		expanded = []
		for key, value in choices.items():
			self.init_skill(key, value)
			pool -= value
		return pool

	def validate_and_set_key(self, key, val, index, selections, group="", destroy=False, custom=False):
		if destroy is True:
			selection = selections.pop(index)
		else:
			selection = selections[index]
		if custom is True:
			self.init_skill(key, value)
			self.skills[key]["pdfslot"] = "Custom"
			return selections
		for item in selection:
			if key == item or group == item or item == "any":
				self.init_skill(key, value)
		return selections

	def request_custom(self, kvpair):
		pass

def gendump(investigator, path):
    path = Path(path)
    if not path.exists():
        path.touch()
    path.write_bytes(pickle.dumps(investigator))

def genload(path):
    path = Path(path)
    if path.exists():
        return pickle.loads(path.read_bytes())

# index, value, custom, group = (val.get("index"), val.get("value"),
			# 			val.get("pdfslot"), val.get("group", ""))
	# if is_occupation is True:
			# 	## break into seperate method?
			# 	if custom is True:
			# 		custom_req = self.request_custom(key, val)
			# 		if custom_req is False:
			# 			raise KeyError(f"You're request for custom skill {key} was denied by the keeper.")
			# 	if index == -1:
			# 		selection = self.occupation.get("skills")
			# 		self.validate_and_set_key(key, value, selection, group="",
			# 				destroy=False, custom=custom)
			# 	else:
			# 		selections = self.validate_and_set_key(
			# 					key, value, index, selections, group=group, custom=custom)
			# else:
			# 	if custom is True:
			# 		custom_req = self.request_custom(key, val)
			# 		if custom_req is False:
			# 			raise KeyError(f"You're request for custom skill {key} was denied by the keeper.")
			# 	self.init_skill(key, value, pdfslot=custom)









