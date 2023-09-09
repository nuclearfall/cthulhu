import cgen
from pprint import pprint
from dataparse import skillroll
from fillpdf import fillpdfs
from pprint import pprint
import json
import random
from functools import reduce
from dataparse import *

random.seed()
# Then damage is dealt to the loser or some other result if neither wins or if not an attack.
def keeper_oppskillroll(inv, invskillname, opp, oppskillname, bonus=0, penalty=0, rolloff=True):
	oppskill = opp.getskill(oppskillname)
	invskill = inv.getskill(invskillname)
	invroll = inv.skillroll(invskill, oppskill, bonus=bonus, penalty=penalty)
	opproll = opp.skillroll(oppskill, invskill)
	is_invwin = request_opposed_skillroll(invroll, opproll)
	print(invskill)
	print(oppskill)
	if is_invwin is None and rolloff is True:
		print("Draw, going again")
		return keeper_oppskillroll(inv, invskillname, opp, oppskillname, bonus=bonus, penalty=penalty)
	else:
		if is_invwin is True:
			return f"{inv.name} Wins!"
		elif is_invwin is False:
			return f"{opp.name} Wins!"
		else:
			return f"We seem to have come to an empasse."

def main():
	# data = fillpdfs.get_form_fields("../data/CharacterSheet.pdf")

	name = "The Amazing Gronzo"

	[cgen.npcgen(f"{i}") for i in range(0, 100)]
	#opp = cgen.npcgen("Hoho Hoooo")
	# invskills = inv.getchars().get("skills")
	# # Sample request made my Keeper class
	# req = make_request(method=inv.skillroll, skill="Dodge", challenge=REGULAR,
	# 		bonus=1)
	# # sample response from investigator.
	# resp = respond(req)
	# print(resp)

	# print(inv.pdfexport())
	# pdfdata = inv.pdfexport()

	# fillpdfs.write_fillable_pdf('../data/CharacterSheet.pdf', 'AmazingGonzo.pdf', pdfdata)
	# cgen.gendump(igen, "AmazingGonzo.cth")



if __name__ == "__main__":
	# for i in range(0, 1000):
		main()