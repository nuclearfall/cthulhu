import json
import skills as skl
from pprint import pprint
import random

with open("../data/occupations.json", "r") as fp:
	occ_defs = json.load(fp)

class Occupation:
	def __init__(self, parent, occ_name, choice=[], mincredit=True):
		self.parent = parent
		self.investigator = parent.investigator
		self.skillset = {}
		self.skillpoints = 0
		if occ_name in occ_defs.keys():
			for key, val in occ_defs.get(occ_name).items():
				setattr(self, key, val)
			if mincredit is True:
				self.skillpoints -= self.mincredit
				self.parent.skills["Credit Rating"] = skl.skill_defs.get("Credit Rating")
				self.parent.skills["Credit Rating"]["value"] += self.mincredit
			self.set_skillpoints()
			#self.set_occupation_skills(choice)
		else:
			raise ValueError(f"{occ_name} is not a valid occupation.")

	def set_skillpoints(self, best=0):
		chars = self.investigator.getchars()
		for scenario in self.scenarios:
			total = 0
			for key, val in scenario.items():
				total += chars.get(key) * val
				if total > best:
					best = total
		self.skillpoints = best 


	def occupation_skills_str(self):
		occ_skills = self.occupation.skills
		choices = self.occupation.selections
		choice_str = ""
		for skill in occ_skills:
			choice_str += f" {skill}"
		if choices:
			choice_str += " and "
			for choice in choices:
				count = choice.get("count")
				selection = choice.get("selections")
				group = choice.get("group")
				if group:
					choice_str += f"{count} from any {group} skill.\n"
				if selection is not None and selection == []:
					choice_str += f"{count} other skills.\n"
				elif selection is not None:
					choice_str += f"{count} from "
					for sel in selection:
						choice_str += f"{sel} "
					choice_str += f"\n"
			return choice_str
	# Skillset is used as an acc.


			
			



	#def set_skills(self, choices=None, skillset={}, count=0, randomness=True):
		
		# selections = self.selections
		# choice_count = sum([sel.get("count") for sel in selections])
		# for name in self.skills:
		# 	skillset[name] = skl.skill_init(name)

		# if selections:
		# 	count = selections[0].get("count")

		# 	while selections:
		# 		# determine valid selections:
		# 		options = self.get_options(0)
		# 		if random and choice_count != 0:
		# 			name = options[random.randrange(0, len(options))]
		# 		elif random:
		# 				break
		# 		else:
		# 			name = choices[choice_count]
			
		# 		if name == "" or name in skillset:
		# 			choice_count -= 1
		# 			count -= 1
		# 		elif name in options:
		# 			choice_count -= 1
		# 			skillset[name] = skl.skill_init(name)
		# 			count -= 1
		# 		else:
		# 			raise ValueError(f"{name} is not a valid selection.")
		# 		if count == 0:
		# 			selections.pop(0)
		# 			count = selections[0] if selections else 0
		# 	print([n for n in skillset])
		# return skillset




# def occupation_names(occupations=occ_defs):
# 	return [o for o in occupations.keys()]

# def skills_list(name, occupations=occ_defs):
# 	return [skill for skill in skills.find(occupations.get(name).get("skills"))]

# def skills_dict(name, occupations=occ_defs):
# 	results = {}
# 	for skill_name in occupations.get(name).get("skills"):
# 		results[skill_name] = skills.find(key="name", val=skill_name)
# 	return results

# def selections(name, occupations=occ_defs):
# 	return occupations.get(name).get("selections")

# def get_occupation(name, occupations=occ_defs):
# 	return occupations.get(name)

# def is_occupation(name, occupations=occ_defs):
# 	return True if occupations.get(name) else False

# 	def skill_point_scenarios(name, occupations=occ_defs):
# 		occupation = occupations.get(name)
# 		return occupation.get("scenarios")

# 	def occupation_skillpoints(occupation, best=0):
# 		for scenario in skill_point_scenarios(occupation):
# 			total = 0
# 			for key, val in scenario.items():
# 				total += stats.get(key) * val
# 				if total > best:
# 					best = total 
# 		return best



if __name__ == "__main__":
	name = "Acrobat"
	job = Occupation(name)
	pprint(job.content)









