from pprint import pprint
from refs import rget, rgetlist
key_container = []

# Recursively checks for unused index and adds to a list.
# by default, mutates the existing key_container.
def setkey(index=0, container=[]):
	k = index or len(key_container)
	if k not in key_container:
		container.append(k)
		return k
	else:
		return get_key(index=len(key_container)+1)

def create_scene(name, parent=None, **kwargs):
	key = setkey()
	template = {
			"key": key,
			"name": name,
			"parent": parent,
			"enter_from": [],
			"exit_to": [],
			"scenes": {},
			"contents": [],
			"occupants": [],
			"description": ""
		}
	# Ensures keys don't begin with a number. 
	return {strkey(key): {**template, **kwargs}}
# level is a str such as "sub". It shouldn't be assigned with an
# initial integer
def strkey(key):
	return f"scene_{key}" if key else None


def keyinfo(str):
	split 
def get_exits(scene):
	return None

scene0 = create_scene("Front Porch", description="Ohhh...scary")
pprint(scene0)

