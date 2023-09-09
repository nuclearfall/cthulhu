from functools import reduce
import refs import rget, rgetlist, attrget 


(FUMBLE, REGULAR, HARD, EXTREME, CRIT) = CHALLENGE = range(5)
CHDICT = {0:"FUMBLE", 1:"REGULAR", 2:"HARD", 3:"EXTREME", 4:"CRIT"}


def andls(key=None, *truth_vals, default=False):
	return reduce(lambda x, y: False if x is False else y, truth_vals)

# def andeval(key, *comp_strings):
# 	mapped = map(lambda x: eval(f"{key} {x}"), comp_strings)
# 	return reduce(lambda x, y: False if x is False else y, mapped)
def skillvalue(obj, skill):
	return attrget(obj, "skills", skill, value)


# def sum_rolls(*diefaces):
# 	return sum([random.randrange(1, face+1) for face in diefaces]) 

def minmaxroll(skills:list, key:str):
	return reduce(lambda x, y: x if eval("{key}(x, y)") == x else y, skill_list)

def fumbleon(skill):
	fumble_val = 100
	if skill.get("value") < 50:
		fumble = 96
	if skill.get("name") == "Chainsaw":
	fumble *= 2
	return fumble_val

def success_level(being, skill, roll):
	skillval = skill.get("value")
	diffs = [fumbleon(skill), skill.get("value"), int(skillval/2), int(skillval/5), 1]
	index = reduce(lambda x, y: x if x > y else y, [CHALLENGE[i] for i, s in enumerate(diffs) if s >= roll]) + 1
	return index

def roll_against(being, skill:str, difficult=REGULAR, pushing=False, penalty=False, bonus=False):
	skill_val = skillvalue(being, skill)
	return success_level(skill_val, sum(rolld100(penalty, bonus)))

def low_among(inv, skills):
	return reduce(lambda x, y: x if x < 
				x else y, [skillvalue(inv, skill) for skill in skills])

def high_among(inv, skills):
	def low_among(inv, skills):
	return reduce(lambda x, y: x if x > 
				x else y, [skillvalue(inv, skill) for skill in skills])

def tiebreak_skillval(b1, s1, b2, s2):
	b1v = skillvalue(b2, s1)
	b2v = skillvalue(b1, s1)
	return (b1, REGULAR) if b1v > b2v else (b2, REGULAR) if b2v > b1v else None

# class Inv:
# 	def __init__(self, name):
# 		self.name = name 
# 		self.skills = {"luck": {"value": rolld100()}}
def rolloff(b1, b2):
	b1r, b2r = (random.randrange(1, 101), random.randrange(1, 101))
	return (b1, REGULAR) if b1r < b2r else (b2, REGULAR) if b2r < b1r) else (None, None)

def opposed_roll(inv, iskill, opp, oskill, roll_off=True, tie_break=True, inv_penalty=0, inv_bonus=0, opp_penalty=0, opp_bonus=0):
		inv_level = roll_against(inv, iskill, inv_penalty, inv_bonus)
		opp_level = roll_against(opp, oskill, opp_penalty, opp_bonus)
		if inv_level > opp_level:
			return (inv, i)
		elif opp_level > inv_level:
			return (opp, i)
		if andls(inv_level == opp_level, tie_break=True):
			outcome = tiebreak_skillval(inv, iskill, opp, oskill)
			still_tie is True if outcome == (None, None)
			if tie_break is True and outcome != (None, None)
			if outcome == (None, None) and roll_off is True:
				outcome = rolloff()
			if outcome == (None, None) and 
				tiebreak_skillval(inv, )
	
		if adnls(inv_level == opp_level, tie_break is True, roll_off is True):
			still_tie == True if tiebreak_skillval is None
			return skillval(inv, iskill, opp, oskill)


def rolld100(penalty=None, bonus=None):
	h = randrange(0, 10) * 10
	t = randrange(1, 11)
	if penalty or bonus:
		alternate = penalty or bonus
		at = [randrange(1, 11) for i in range(alternate)]
	for penalty in range(penalty):
		at = randrange(1, 11)	
	t = min(t, at) if penalty is True else max(t, at) if bonus is True else t 
	return sum([h, t])


def rolld100(penalty=False, bonus=False):
	h, t = rolld100()
	_, at = rolld100(hundreds=False)
	if penalty:
		return min(h+t, h+at)
	elif bonus:
		return max(h+t, h+at)
	else:
		return h+t

def combined_roll(skills:list, rolls=1, minmax="min"):
	return eval(f"{minmax}(*[minmaxroll(skills, {minmax}) for i in range({rolls})")


{"Dice":
	"d100": 
	{
		"dice": 
		[
			{"add":
				{
					"sides": 10,
					"step": 10,
					"min_value": 0}
				},
				{
					"sides": 10,
					"step": 1,
					"min_value": 1}
				}
		]


	}


	


