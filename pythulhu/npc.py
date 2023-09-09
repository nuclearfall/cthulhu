import refs
import roll
import generator as gen


def npcgen(**kwargs):
	npc = gen.chargen(**kwargs)
	passargs = kwargs.get("passargs")
	char = withrolledchars()

	char["age"] = kwargs.get("age", randomage(char))
	char["occuapation"] = kwargs.get("occupation", random.choice(
			[o for o in occs().keys()]))

	for k, v in kwargs.items():
		if k in gen.character_template().keys():
			char[k] = v

	for fn, args in passargs.items():
		char = fn(char, **args)

	return char

def npcgen(**kwargs):
	npc = gen.chargen(**kwargs)
	for k, v in kwargs.items():
		if k in gen.character_template().keys():
			char[k] = v
	skills = {}

	language = kwargs.get("language", "English")
	chars = rollchars()
	for char, roll in chars.items():
		setattr(character, char, roll)

	set_occ(kwargs.get("occupation", None), mincredit=kwargs.get("mincredit", True))	
	age = random_age()
	set_age_reference()
	age_adjust()
	is_age_adjusted = True
	set_secondary_chars()
	random_set_skills()
	character.skills = skills
	set_wealth()
	character.dodge = skills.get("Dodge")

	return character

def randomage(character):
	return random.choices(population=[random.randrange(15,20), random.randrange(20,40), 
			random.randrange(40,50), random.randrange(50,60), random.randrange(60,80)], 
			k=1, weights=[0.02, 0.65, 0.2, 0.1, 0.05])[0]