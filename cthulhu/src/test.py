import cgen
from pprint import pprint

from fillpdf import fillpdfs
from pprint import pprint
import json
from functools import reduce



def main():
	data = fillpdfs.get_form_fields("../data/CharacterSheet.pdf")

	name = "The Amazing Gronzo"
	occupation = "Acrobat"
	age = 24
	igen = cgen.InvestigatorGen(name, age, occupation)
	#igen = cgen.genload("AmazingGonzo.cth")
	inv = igen.investigator
	# RESET FOR TESTING
	igen.skills = {}
	igen.occ_skillpoints = 260
	igen.pi_skillpoints = 170

	inv.language = "English"
	inv.backstory = "I was born in a small village in Russia. I have mostly forgotten my language, but I'll never my homeland. My life is spent as a performer in a traveling circus. Everywhere I go, I know someone."
	inv.birthplace = "Petrograd, Russia"
	inv.residence = "Everytown, USA"

	#igen.skills["Dodge"] = {"name": "Dodge", "value": 0, "parent": None, "pdfslot": "Dodge"}
	# Passing set_skills without any arguments returns skillpoint assignments yet to be made.
	#print(igen.set_skills())
	#### WARNING! ####
	# Does not check if skill is in skillset to assigne values.
	# 260 SKill Points to assign to Gonzo
	occ_assignments = {"Occupation": {
		"Credit Rating": 5,
		"Climb": 30,
		"Jump": 30,
		"Spot Hidden": 50,
		"Fast Talk": 50,
		"Swim": 20,
		"Dodge": 40,
		"Russian": 15,
		"Throw": 10,
		"Dodge": 10
		}}

	igen.set_skills(occ_assignments)

	# Wow, my math sucks...
	occ2_assignments = {"Occupation": {
		"Dodge": 10,
		"Throw": 30
		}}
	igen.set_skills(occ2_assignments)

	print(igen.set_skills())	
	# # 170 PI Points
	pi_assignments = {"Personal Interest": {
		"Handgun": 40,
		"Brawl": 50,
		"Sleight of Hand": 30,
		"Appraise": 20,
		"Diving": 20

	}}
	#print(inv.dodge)
	igen.set_skills(pi_assignments)

	pi2_assignments = {"Personal Interest": {
		"Jump": 10
	}}

	igen.set_skills(pi2_assignments)	
	pprint(igen.set_skills())
#	pprint(inv.skills)
	# print(inv.pdfexport())
	pdfdata = inv.pdfexport()

	fillpdfs.write_fillable_pdf('../data/CharacterSheet.pdf', 'AmazingGonzo.pdf', pdfdata)
	cgen.gendump(igen, "AmazingGonzo.cth")



if __name__ == "__main__":
	# for i in range(0, 1000):
		main()