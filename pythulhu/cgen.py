import json
import random
import fillpdf
import refs
from refs import *
from pprint import pprint
from fillpdf import fillpdfs
import skills as skl
import occupations as occ
import character
from occupations import Occupation
from skills import getslots, is_parent, children, getskval
# from refs import genref, occref, skillref, topdftemp, svalget
from functools import reduce
from pathlib import Path
from copy import deepcopy
random.seed()

_primary = ["pow", "str", "con", "dex", "app", "siz", "edu", "int"]


def validate_input(data, typeof=[dict, tuple, list], fn=None, error=""):
	try:
		if type(data) in typeof:
			return fn(data) if fn else data
	except:
		raise ValueError(error)

class CharacterGen:
	def __init__(self, inv, name, language="English",
				age_adjustment=None, occ_skill_choices=[], era=0,
				presets=None, pdf=None, **kwargs):
		self.is_age_adjusted = False
		self.era = era
		self.name = name
		self.age = kwargs.get("age", None)
		self.language = language
		self.skills = {}
		if presets:
			for key, preval in presets.items():
				if key in topdftemp.values():
					setattr(self.character, key, preval)
					self.age_adjusted = True
		self.occ_skillpoints = 0
		self.skillpoints = 0
		self.character = None
		self.skills = {}

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
		credit = attrget(self, "skills", "Credit Rating", "value")
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

	def age_adjust(self, choices=None, age=30, random_age=False):
		self.set_age_reference()
		if random_age is True:
			self.set_age_reference()
			selection = self.penalties
			decisions = []
			for penalty in selection:
				if len(penalty) > 2:
					points, *stats = penalty
					distro = refs.constrained_pos_sum(len(stats), abs(points))
					choices = list(zip(stats, distro))


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

	def generate_random(self, **kwargs):
		self.occ_skillpoints = 0
		self.skillpoints = 0
		self.character = None
		self.skills = {}
		self.character = character.Investigator(name=self.name,
				language=kwargs.get("language"), **kwargs)
		self.language = kwargs.get("language", "English")
		chars = self.rollchars()
		for char, roll in chars.items():
			setattr(self.character, char, roll)
		# set occupation, skillpoints if occupation isn't set, then set randomly
		self.set_occ(kwargs.get("occupation", None), mincredit=kwargs.get("mincredit", True))	
		self.age = self.random_age()
		self.set_age_reference()
		self.age_adjust()
		self.is_age_adjusted = True
		self.set_secondary_chars()
		self.random_set_skills()
		self.character.skills = self.skills
		self.set_wealth()
		self.character.dodge = self.skills.get("Dodge")

		return self.character


	def generate(self, **kwargs):
		self.occ_skillpoints = 0
		self.skillpoints = 0
		self.character = None
		self.skills = {}
		if kwargs.get("random"):
			return self.generate_random(**kwargs)
		self.language = kwargs.get("language", "English")
		self.character = character.Investigator(name=self.name, age=self.age, 
				language=kwargs.get("language"), **kwargs)
		self.rollchars()
		self.age = kwargs.get("age", self.age)
		self.age_adjust(kwargs.get("age_adjustments"))
		self.set_secondary_chars()
		# set occupation, skillpoints
		self.set_occ(kwargs.get("occupation", self.occname))
		# allow players to revisit with skill selections.
		if kwargs.get("skill_selection", None) or kwargs.get("random_skills"):
			# skill selection should either be a dict of skill:value pairs or
			# "random_skills=True
			self.skillpoints = self.character.int * 2
			self.set_skills(choices=kwargs.get("skill_selections", None))
			self.set_wealth()
			self.character.skills = self.skills
			self.character.dodge = self.skills.get("Dodge")
			return self.character
		else:
			return None

	def set_occ(self, occname=None, custom=False, mincredit=True, occmin=0):
		if occref.get(occname):
			self.occname = occname
			self.character.occupation = occname
		else:
			self.occname = occname = random.choice([occ for occ in occref if occref[occ].get("era") == self.era])
			self.character.occupation = occname
		
		occmin = 0 if not mincredit else rget(occref, occname, "mincredit")
		self.occ_skillpoints = self.set_occskillpoints(occname)
		self.init_skill("Credit Rating", value=occmin)

	def set_occskillpoints(self, occname):
		scenarios = []

		for scenario in rget(occref, occname, "scenarios"):
			scenario_vals = []
			for key, val in scenario.items():
				scenario_vals.append(self.chars.get(key) * val)
			scenarios.append(sum(scenario_vals))

		return max(scenarios)

	def init_skill(self, key:str, value=0, pdfslot=None, max_skill=99,
				keys=["name", "parent", "value", "pdfslot", "checked", "custom"]):
		if not key in self.skills:
			self.skills[key] = skillref[key]
		start_val = self.skills.get("value", 0)
		if value + start_val > max_skill:
			raise ValueError(f"Assignment exceed maximum for {key}: {value} and {start_val}")
		self.skills[key]["value"] += value

	def expand_choices(self, selection, acc=[], index=0):
		if is_group(item):
			acc = acc + [m for m in members(item) if m not in acc]
		elif is_parent(item):
			acc = acc + [c for c in children(item) if c not in acc]
		else:
			acc = acc + [item] if item not in acc else acc
		return acc

	def constrained_sum(self, n, total):
		dividers = sorted(random.sample(range(1, total), n - 1))
		return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

	# def safe_constrained(self, n, total, initvals, maxper=75, remains=None):
	# 	vals = self.constrained_sum(n, total)
	# 	remains = sum([sum(x)-maxper for x in zip(initvals, vals) if sum(x) > maxper])
	# 	index = 0
	# 	while remains > 0:
	# 		vals = self.constrained_sum(n, total)
	# 		remains = sum([sum(x)-maxper for x in zip(initvals, vals) if sum(x) > maxper])
	# 		index += 1
	# 		if index > 20:
	# 			break
	# 	if remains > 0:
	# 		return None
	# 	else:
	# 		return vals

	def skills_from_selections(self, selections):
		choices = []
		for selection in selections:
			if selection == ["All"]:
				choices.append(random.choice(skl.chargen()))
			else:
				choices.append(random.choice(selection))
		return self.specialize(choices)

	def specialize(self, choices):
		specialized = []
		for choice in choices:
			if skl.is_parent(choice):
				options = skl.children(choice)
				specialized.append(random.choice(options))
			else:
				specialized.append(choice)
		return specialized
	# check skills before looking up initial value
	def get_skillval(self, name):
		try:
			return self.skills.get(name).get("value") if self.skills.get(name) else rget(skillref, name, "value")
		except:
			raise KeyError(f"{name} isn't init'ed or isn't in skill reference.")

	def reallocate(self, overflow, inits, vals, maxper=75):
		index = 0
		temp_vals = []
		while overflow > 0 or index < len(vals):
			print("am i stuck?")
			ival = inits[index]
			val = vals[index]
			total = ival+val
			cantake = maxper - total 
			print("can take", cantake)
			if cantake > 0:
				if cantake > overflow:
					val += overflow
					overflow = 0
				else:
					val += cantake
					overflow -= cantake
			temp_vals.append(val)
			index += 1
		return temp_vals

	def safeinit_random_skills(self, skill_list, skillpoints, maxper=75):
		skill_count = len(skill_list)
		init_values = [self.get_skillval(s) for s in skill_list]
		skill_values = self.constrained_sum(len(init_values), skillpoints)
		# its possible allocation results in values > maxper:
		overflow = sum([sum(x)-maxper-x[0] for x in zip(init_values, skill_values) if sum(x) > maxper])
		if overflow > 0:
			print(overflow)
			skill_values = self.reallocate(overflow, init_values, skill_values, maxper)
		[self.init_skill(s, value=v) for s, v in zip(skill_list, skill_values)]

	def random_set_skills(self, exclude=["Cthulhu Mythos"], maxper=75):
		self.edgecases()
		occ_skills = rget(occref, self.occname, "skills") + ["Credit Rating"]
		occ_skills += self.skills_from_selections(rget(occref, self.occname, "selections"))

		skillpoints = int(self.character.int * 2)
		pi_skills = [random.choice([k for k in skillref.keys(
				) if k not in self.skills and k not in exclude]) for i in range(int(skillpoints / 15))]
		self.safeinit_random_skills(pi_skills, skillpoints)
		pprint([(k,v.get("value")) for k, v in self.skills.items()])

		return None

	# Check for malformed data here:
	def set_skills(self, choices):
		occ_choices = choices.get("Occupation")
		pi_choices = choices.get("Personal Interest")
		if not choices:
			return f"{self.skillpoints} occupation skill points and {self.skillpoints} personal interest skillpoints remain to assign."
		if not self.skills:
			[self.init_skill(key) for key in occref.get("skills")]
		# Step through and wait for all skill decisions to be made before moving on.
		if occ_choices:
			self.occ_skills = self.from_selections(occ_choices, "skillpoints")
			if self.skillpoints > 0:
				return f"{self.skillpoints} occupation skillpoints remain to assign"
		if pi_choices:
			pi_selections = [{"count": 99, "selections": []}]
			if self.skillpoints > 0:
				return f"{self.skillpoints} personal interest skillpoints remain to assign."
		if self.skillpoints == self.skillpoints == 0:
			[self.init_skill(k) for k, v in skillref.items() if v.get("pdfslot") and v.get(
					"pdfslot") not in getslots() and k not in self.skills and v.get("era") == 0]
			self.edgecases()
			return True
		return None

	def edgecases(self):
		dkey, dval, okey, oval = ("Dodge", int(self.character.dex/2), "Own Language", self.character.edu)
		self.init_skill("Own Language", value=oval)
		self.init_skill("Dodge", value=dval)
		self.init_skill("Brawl")
		print("Set", dkey, dval, okey, oval, "Brawl", rget(skillref, "Brawl", "value"))

	def from_selections(self, choices:dict, pool:int, max_skill=99):
		pool = getattr(self, pool)
		expanded = []
		for key, value in choices.items():
			self.init_skill(key, value)
			pool -= value
		return pool

	def request_custom(self, kvpair):
		pass

def npcgen(name="Non Player Character"):
	npcgen = deepcopy(CharacterGen(name))
	npcgen.generate(random=True)
	npc = npcgen.character
	return npc



def gendump(investigator, path):
    path = Path(path)
    if not path.exists():
        path.touch()
    path.write_bytes(pickle.dumps(investigator))

def genload(path):
    path = Path(path)
    if path.exists():
        return pickle.loads(path.read_bytes())









