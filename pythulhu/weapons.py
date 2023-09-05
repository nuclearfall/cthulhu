import json

with open("../data/weapons.json") as fp:
    weapon_ref = json.load(fp).get("weapons")
def weapon_str(wname, key="name", cond=True):

	for val in weapon_ref:
		name = val.get("name")
		ident = val.get(key)
		if isinstance(ident, int):
			ident = str(ident).lower()
			wname = wname.lower() 

		if wname in ident:
			skill = val.get("skill") # requires skill lookup for s/h/f
			damage = val.get("damage")
			attacks = val.get("attacks")
			srange = val.get("range")
			ammo = val.get("ammo")
			malfunction = val.get("malfunction")
			print(f"""
Name: {name}
Skill: {skill},
Attacks: {attacks},
Range: {srange},
Ammo: {ammo},
Malfunction: {malfunction}
""")
			return (name, skill, damage, srange, ammo, malfunction)


weapon_str("100", key="range")
