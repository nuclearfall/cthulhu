import refs as refs
import random
import roll
import generator as gen
import skills as skl 
import occupations as occ
from pprint import pprint

def randomname(sex=None):
	sex = sex or random.choice(["male", "female"])
	male, female, surname = zip(*refs.nameref.values())
	if sex == "male":
		male, surname = random.choice(male), random.choice(surname)
		return f"{male} {surname}"
	else:
		female, surname = random.choice(female), random.choice(surname)
		return f"{female} {surname}"

def randomage():
	return random.choice(random.choices(population=[random.randrange(15,20), random.randrange(20,40), 
						random.randrange(40,50), random.randrange(50,60), random.randrange(60,80)], 
						k=1, weights=[0.02, 0.65, 0.2, 0.1, 0.05]))

def randomageadjust(char, ref=gen.genref):
	if char.get("age") in range(15,20):
		return gen.teenage_development(char, dict(zip(["str", "siz"], [-2, -3])))
	elif char.get("age") in range(20,40):
		return gen.improvement_check(char)
	else:
		points = gen.outofprime_choicecalc(char.get("age"))
		changes = dict(zip(["str", "dex", "con"], refs.constrainedsum(3, points)))
		char = gen.outofprime(char, changes)
		return gen.improvement_check(char)

#### Random Skills ####
def reallocate(overflow, skilllist, inits, vals, maxper=75):
	index = 0
	temp_vals = []
	while overflow > 0 and index < len(vals):
		ival = inits[index]
		val = vals[index]
		total = ival+val
		cantake = maxper - total 
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

def initrandomskills(char, skill_list, skillpoints, maxper=75, era=0):
	skill_count = len(skill_list)
	for skill in skill_list:
		if not skl.skillref.get(skill):
			raise KeyError(f"{skill} is invalid")
	init_values = [gen.getcharskillval(char, s) for s in skill_list]
	skill_values = refs.constrainedsum(len(init_values), skillpoints)
	poss_overflow = map(sum, zip(init_values, skill_values))
	overflow = sum([x-maxper for x in poss_overflow if x > maxper])
	if overflow > 0:
		skill_values = reallocate(overflow, skill_list, init_values, skill_values, maxper)
	skills = {k:{"value": v, "checked": False} for k, v in zip(skill_list, skill_values)}
	return skills

def setrandomskills(char, exclude=["Cthulhu Mythos"], mincredit=True, maxper=75):
	skills = gen.initskills(char)
	occskillpoints = gen.occskillpointscenarios(char)
	if mincredit is True:
			lowcredit = refs.rget(refs.occref, char.get("occupation"), "mincredit", default=0)
			if lowcredit is None:
				raise ValueError(f"{char.get('occupation')} seems to have no lowcredit.")
			char["skills"]["Credit Rating"] = {"value": lowcredit, "checked": False}
			occskillpoints -= lowcredit
	occ_skills = refs.rget(refs.occref, char.get("occupation"), "skills") + ["Credit Rating"]
	occ_skills += randomskillselections(char, refs.rget(refs.occref, char.get("occupation"), "selections"))
	occ_skills = initrandomskills(char, occ_skills, occskillpoints)
	piskillpoints = char.get("int") * 2
	pi_skills = [random.choice([k for k in refs.skillref.keys() if k not in char.get(
				"skills") and k not in exclude]) for i in range(int(piskillpoints / 15))]
	pi_skills = initrandomskills(char, pi_skills, piskillpoints)
	return {**char, **{"skills": {**skills, **occ_skills, **pi_skills}}}

def randomskillselections(char, selections):
	choices = []
	if not selections:
		return []
	for selection in selections:
		if selection == ["All"]:
			choices.append(random.choice([k for k, v in refs.skillref.items(
						) if not skl.is_parent(k) and gen.iscommonskill(char, k, v)]))
		else:
			choices.append(random.choice(selection))
	return specialize(char, choices)

def specialize(char, choices):
		specialized = []
		for choice in choices:
			if skl.is_parent(choice):
				options = skl.children(choice)
				specialized.append(random.choice(options))
			else:
				specialized.append(choice)
		return specialized

def chargen(**kwargs):
	char = gen.chargen(**kwargs, isageadjusted=False)
	has_name, has_age, has_occupation, has_skills = (char.get("name"), char.get("age"), 
				char.get("occupation"), char.get("skills"))
	passargs = kwargs.get("passargs")
	char = gen.withrolledchars()
	for k, v in kwargs.items():
		if k in gen.character_template().keys():
			char[k] = v
	char["name"] = kwargs.get("name", randomname(sex=kwargs.get("sex", None)))
	char["age"] = kwargs.get("age", randomage())
	randomageadjust(char)
	char["occupation"] = kwargs.get("occupation", random.choice(
			[o for o in refs.occref.keys()]))
	char = gen.secondarychars(char)
	if not has_skills:
		char = {**char, **{"skills": gen.setstatbasedskills(char)}}
		char = setrandomskills(char)
	return char

npc = chargen(name="George")

#gen.ppfields(npc, ["Dodge", "dodge", "Own Language"])
#npcs = [npcgen() for i in range(0, 1000)]


# 	language = kwargs.get("language", "English")
# 	chars = rollchars()
# 	for char, roll in chars.items():
# 		setattr(character, char, roll)

# 	set_occ(kwargs.get("occupation", None), mincredit=kwargs.get("mincredit", True))	
# 	age = random_age()
# 	set_age_reference()
# 	age_adjust()
# 	is_age_adjusted = True
# 	set_secondary_chars()
# 	random_set_skills()
# 	character.skills = skills
# 	set_wealth()
# 	character.dodge = skills.get("Dodge")

# 	return character
