# The goal of the map class is to allow players to explore
# while the keeper goes about the business of minding the
# rest of the sandbox.

# All I need right now is something that allows people to
# change positions form one to another? Can you do that.
# If you press n can you go the next more northern position?
from uuid import uuid4

RELATIVE = ["front", "back", "left", "right", "up", "down"]
OPPOSITE = ["back", "front", "right", "left", "down", "up"]

class SceneMap:
	def __init__(self, name="Map", start=None):
		start_address = (0, 0, 0)
		self.scenemap = {}
		self.passthru = {}
		self.add(Scene(name="Start"))
	def setatkv(self, key, val):
		self.scenemap[key] = val
	def add(self, scene):
		# new locations must be related to a location currently on the map.
		if not scene.address:
			sx, sy, sz = address = (0, 0, 0)
			#how can I stretch a node to include a range?
			for key, loc in scene.neighbors().items():
				if key == "infrontof" and loc:
					lx, ly, lz = loc.address
					address = (lx+1, ly, lz)
					loc.setatkv("behind", scene)
				if key == "behind" and loc:
					lx, ly, lz = loc.address
					address = (lx-1, ly, lz)
					loc.setatkv("infrontof", scene)
				if key == "toleftof" and loc:
					lx, ly, lz = loc.address
					address = (lx, ly-1, lz)
					loc.setatkv("torightof", scene)
				if key == "torightof" and loc:
					lx, ly, lz = loc.address
					address = (lx, ly+1, lz)
					sy = ly - 1
					loc.setatkv("toleftof", scene)
		else:
			address = scene.address
		if address in self.addresses():
			raise KeyError(f"Node {scene.name} with key {address} exists in scenemap. Must remove that node first.")
		scene.setatkv("address", address)
		self.setatkv(str(scene.address), scene)
		return scene
	def allow_passthru(self, scene1, scene2):
		#while 2 locations may be physically next to each other, they may not permit movement between.

		pass 
	def relations(self):
		min_x = min([val.address[0] for val in self.scenemap.values()])
		max_x = max([val.address[0] for val in self.scenemap.values()])
		min_y = min([val.address[1] for val in self.scenemap.values()])
		max_y = max([val.address[1] for val in self.scenemap.values()])
		blank = " "
		map_str = ""
		i = 0
		replace_c = []
		last_location_x = 0
		lvy = 0
		for j in range(min_y, max_y+1):
			for i in range(min_x, max_x+1):
				address = (i, j, 0)
				location = self.scenemap.get(str(address), "")
				if location:
					map_str += str(location)
				else:
					map_str += "                       "
			last_location_x = 0
			map_str += "\n"

		print(replace_c)
		return map_str

	def addresses(self):
		return [val.address for val in self.scenemap.values()]

		
class Scene(SceneMap):
	def __init__(self, name, **kwargs):
		self.scene_dict = {
				"name": "",
				"address": "",
				"end_address": "",
				"description": "",
				"infrontof": None,
				"behind": None,
				"toleftof": None,
				"torightof": None,
				"topof": None,
				"bottomof": None,
				"contents": [],
				"others": [],
				"portals": [],
				"length": 1,
				"width": 1,
				"depth": 1
				"enterfrom": None
				"exitto": None
			}
		for k in self.scene_dict.keys():
			self.setatkv(k, kwargs.get(k, self.scene_dict.get(k)))
		self.setatkv("name", name)
	def __str__(self):
		return f"|=== {self.name:14}===|"
	def setatkv(self, key, val):
		setattr(self, key, val)
		self.scene_dict[key] = val	
	def neighbors(self): 
		return {k:getattr(self, k) for k in [
				"infrontof", "behind", "toleftof", "torightof", "topof", "bottomof"]}

class FiniteStateDevice:
	door = False
	window = False
	stairs = False
	hatch = False

scenemap = SceneMap("Map")
# scene0 = scenemap.scenemap.get("(0, 0, 0)")
# scene1 = Scene("New Scene", toleftof=scene0)
# scenemap.add(scene1)
# scene2 = Scene("Next Scene", toleftof=scene1)
# scenemap.add(scene2)
# scene3 = Scene("Then Scene", behind=scene1)
# scene4 = Scene("Some Scene", behind=scene3)
# scene5 = Scene("Might Scene", torightof=scene4)
# scene6 = Scene("Right Scene", torightof=scene0)
# scene7 = Scene("Mostly Scene", torightof=scene6)
# scene8 = Scene("Contains...", behind=scene7)
# scene9 = Scene("Some Scene", infront=scene3)

addresses = [(i, j, z) for i in range(0, 11) for j in range(0, 11) for z in range(-1, 3)]
middle_point = (4, 4)

print(addresses)
[]
# scenemap.add(scene3)
# scenemap.add(scene4)
# scenemap.add(scene5)
# scenemap.add(scene6)
# scenemap.add(scene7)
# scenemap.add(scene8)

print(scenemap.relations())
enterscenefrom =
exitsceneto = 

f"""              		
|=^ Start=|->  
         ^

"""