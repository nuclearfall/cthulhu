from pprint import pprint
import random
from functools import reduce


CRIT = 0
EXTREME = 1
HARD = 2
REGULAR = 3
FAIL = 4
FUMBLE = 5

ChallengeLevel = {5:"FUMBLE", 4: "FAIL", 3:"REGULAR", 2:"HARD", 1:"EXTREME", 0:"CRIT"}
[random.seed() for i in range(0, 10)]

def dtens(fn=max, count=1):
	return dunits(count=count, lowval=0, highval=90, step=10, fn=fn)
	
# dunits has a lot of super extra flags, but can do a lot of really cool things taking **kwargs from a dict
def dunits(lowval=1, highval=10, fn=max, step=1, count=1, add=0, sub=0, mul=1, div=1, lim=99, flr=1):
	return fn([max(min((int(random.randrange(lowval, highval+1, step=step)*mul/div)+add-sub), lim), 1) for i in range(count)])

def sumxdn(count=1, highval=10, addmod=0, submod=0):
	return dunits(count=count, highval=highval, fn=sum) + addmod - submod

# modify addmod by modvalue / moddivideby 
def mod_sumxdn(modvalue=0, moddividedby=1, **kwargs):
	return sumxdn(**{**{"addmod": max(int(
			modvalue/moddivideby), 1)+kwargs.get("addmod", 0)}, **kwargs})

def d100(count=1, fn=max):
	return 0 if count == 0 else fn(dtens(count=count)) + dunits()

def d100penalty(count=1):
	return d100(count, fn=min)

def fumblerange(skill):
	minfumble = 96 if skill.get("value") < 50 else 100
	return minfumble if skill.get("name") != "Chainsaw" else (
			92 if skill.get("value") < 50 else 99)

def skillroll(skill=None, challenge=REGULAR, bonus=0, penalty=0):
	fn = min if penalty else max
	roll, level = successlevel(roll=dtens(count=(bonus or penalty)+1, fn=fn) + dunits(),
			val=skill.get("value"), fumble=fumblerange(skill))
	return {"roll": roll, "name": skill.get("name"), "value": skill.get("value"), 
				"level": ChallengeLevel.get(level), "pass": passfail(level, challenge)}

def successlevel(roll, val, fumble):
	sl_range = successrange(val, fumble)
	level = sl_range.index(reduce(lambda x, y: x if roll in x else y, sl_range))
	return (roll, level)

def successrange(val, fumble):
	return [[1], range(1, int(val/5)+1), range(int(val/5)+1,int(val/2)+1), 
			range(int(val/2)+1, val+1), range(val+1, fumble), range(fumble, 101)]

def passfail(level, challenge):
	return True if level <= challenge else False

def targetlevel(value):
	return REGULAR if value in range(0, 50) else HARD if value in range(50, 90) else EXTREME

def opposed_skillroll(skill=None, oppskill=None, bonus=0, penalty=0):
	targetlevel = oppskill.get("value")
	return skillroll(skill, challenge=targetlevel, penalty=penalty, bonus=bonus)

# Sends request json recieves json resp
# {
#	"request": request_opposed_skillroll()
#	"id": name
#	
# }
# For Keeper.oppposed_skillroll. Makes calls to investiagtor and opponent objects and evaluates
# Keeper method will make recursirve calls to this if they don't want an impasse. 


def request_opposed_skillroll(invskillroll=None, oppskillroll=None):
	roll, skill, sl, pf = invskillroll
	oroll, oskill, osl, opf = oppskillroll
	if not pf and not opf:
		return None
	if pf and not opf:
		return True
	if opf and not pf:
		return False
	else:
		if sl > osl:
			return True
		if sl < osl:
			return False 
		else:
			return tiebreaker(skill.get("value"), oskill.get("value"))

# Tiebreaker returns True if investigator wins.
def tiebreaker(skillval, oppskillval):
	if skillval > oppskillval:
		return True
	elif skillval < oppskillval:
		return False
	else:
		# if skill values are equal, recursively rolloff until there is a winner.
		return None

def make_request(**kwargs):
	return kwargs

def respond(reqdict):
	reqdict = reqdict
	meth = reqdict.get("method")
	kwargs = {}
	for key,val in reqdict.items():
		if key != "method":
			kwargs[key] = val
	return meth(**kwargs)



	











	