from functools import reduce
import refs

(FUMBLE, REGULAR, HARD, EXTREME, CRIT) = CHALLENGE = range(5)
CHDICT = {1:"FUMBLE", 2:"REGULAR", 3:"HARD", 4:"CRIT"}

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

def andls(key=None, *truth_vals, default=False):
	return reduce(lambda x, y: False if x is False else y, truth_vals)

def andeval(key, *comp_strings):
	mapped = map(lambda x: eval(f"{key} {x}"), comp_strings)
	return reduce(lambda x, y: False if x is False else y, mapped)



def sum_rolls(*diefaces):
	return sum([random.randrange(1, face+1) for face in diefaces]) 

def minmaxroll(skills:list, key:str):
	[getattr(inv, "skills", skill) for skill in skills]
	return eval(f"reduce(lambda x, y: x if x {operator} y else y, skills)"
		
def reference(ref, *args, return_list=False):
	if arg_list:
		return rgetlist(ref.get_ref(ref), *args))
	else:
		return rget(ref, *args))

def success_levels(skill, roll):
	diffs = [96, skill, int(skill/2), int(skill/5), 1]
	# map_diff = map(lambda x: True if roll <= x else False, [1,  int(skill/5), int(skill/2), skill, 96])
	# # list(map(lambda x: x if True else ~x, map_diff))
	index = reduce(lambda x, y: x if x > y else y, [CHALLENGE[i] for i, s in enumerate(diffs) if s >= roll])
	return index



# def difficulty(modroll, challenge, diff=REGULAR):
# 	 = [False for i in range(5)]
# 	if roll == 100:
# 		return [True for i in range(5)]
# 	else:
# 		if not diff or REGULAR:f
# 			pass_level = [True, True, False, False, False]
# 	if int(roll / 2) < challenge:
# 		pass_level = REGULAR 

def roll_against(being, skill:str, difficult=REGULAR, pushing=False, penalty=False, bonus=False):
	skill_val = attrget(being, "skills", skill, "value")
	return success_level(skill_val, sum(rolld100(penalty, bonus))

def low_among(investigators, skill):
	return reduce(lambda x, y: x if rget(getattr(x, "skills"), skill, "value") < rget(
				getattr(y, "skills"), skill, "value") else y, investigators)

def high_among(investigators, skill):
	return reduce(lambda x, y: x if rget(getattr(x, "skills"), skill, "value") > rget(
				getattr(y, "skills"), skill, "value") else y, investigators)

def high_skill(b1, s1, b2, s2):
	b1v = attrget(b1, "skills", s1, "value")
	b2v = attrget(b1, "skills", s1, "value")
	return b1 if b1v > b2v else b2 if b2v > b1v else None

class Inv:
	def __init__(self, name):
		self.name = name 
		self.skills = {"luck": {"value": rolld100()}}

def opposed_roll(inv, iskill, opp, oskill, roll_off=True, penalty=False, bonus=False):
		inv_level = roll_against(inv, iskill, penalty, bonus)
		opp_level = roll_against(opp, oskill)
		tie_break = high_skill(inv, inv_skill, opp, oskill)
		elif inv_level > opp_level:
			return inv
		elif opp_level > inv_level:
			return opp 
		else:
			if andls(inv_level == opp_level, tie_break is None, roll_off is True):
				return opposed_roll(inv, iskill, opp, oskill)
			elif andls(inv_level == opp_level, tie_break is None, roll_off is False):
				return None
			else:
				return tie_break

def rolld100(penalty=None, bonus=None):
	h = randrange(0, 10) * 10
	t = randrange(1, 11)
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





	


