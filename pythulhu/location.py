from typing import NewType
from uuid import uuid4
import refs

class ScenarioMap:
	def __init__(self, name, start=(0,0,0), locations=[], inside={},
			noneuclidean=False):
		self.connections = {
				"x":[],
				"y":[],
				"z":[],		
			}
		self.locations = []
		self.removed = []

	def to_json(self):
		json_map = {}
		for key, item in self.__dict__.items():
			if isinstance(item, GameMap):
				to_json(item)
			else:
				json_map[key] = item

	def lidtoxyz(self, lid):
		return tuple(map(int, lid.split("_")[1:]))

	def xyztolid(self, xyz):
		x, y, z = xyz
		return f"{self.name}_l_{x}_{y}_{z}"

	def remove(self, lid):
		location = reduce(lambda x, y: x if x.lid == lid else y, self.locations)
		self.locations.pop(index(location))
		self.removed.append(location)

	def insert(self, obj):
		if not obj in self.locations:
			location.parent = self
			self.locations.append(location)
			return [l.name for l in self.locations]
	def insert(self, axrange):



	def reposition(self, location, xyz):
		location.setxyz(*xyz)
		new_lid = self.lidfromxyz(new_xyz)
		if not new_xyz_str in self.locations:
			self.remove_location(location.lid)
			self.insert_location(location.lid)

	def conkey(self, current): 
		return (f"{current.lid}", None)

	def connect(self, current, new, portal):
		if self.is_adjacent(current, new):
			axis = adjacent_on(current, new)
		if cex is not False and nen is not False:
			cton = f"{current.lid}_to_{new.lid}_{axis}_through_{portal.lid}"
		if cen is not False and nex is not False:
			ntoc = f"{new.lid}_to_{current.lid}_{axis}"
		if nex is False or cen is False:
			ntoc = f"{new.lid}_not_to_{current.lid}_{axis}"
		if cex is False or nen is False:
			cton = f"{current.lid}_not_to_{new.lid}"
		return 

	def adjacent_on(self, current, new):
		if current.noneuclidean is True or new.noneuclidean is True:
			return "on_noneuclidean_axis"
		if current.z in [new.z+1, new.z-1] and (current.x == new.x or current.y == current.y):
			return "on_z_axis"
		elif current.y == new.y:
			return "on_y_axis"
		elif current.x == new.x:
			return "on_x_axis"
		else:
			return None

	def is_connected(self, current, new):
		if is_adjacent(current, new) and currrent.connections.get(new.lid):
			return True
		else:
			return refs.trueforone([True for k in self.conkeys(current=current, new=new) if k in self.connections])

	def connect(self, current, new, cflags, nflags):
		if self.is_adjacent(self, new):
			axis = self.adjacent_on(current, new)
			constrings = self.conkeys(current=current, new=new)
			if new not in self.locations:
				self.locations.append(new)
			if current not in self.locations:
				self.locations.append(new)
			self.connections[axis] += constrings
		else:
			raise KeyError(f"Location {new.locid} is not adjacent to current {self.locid}")

	def add_portal(self, axis, exit=True, enter=True, location=None):
		self.connections[axis] += self.conkeys(self, location)


# A Location can be a game map within a greater game map. This allows for buildings within.
class ScenarioLocation(ScenarioMap):
	def __init__(self, name, parent=None, x=0, y=0, z=0,
			is_map=False, items={}, description="", starting_loc=False,
			no_connect=False, auto_connect=True):
		super().__init__(self, name)
		self.name = name
		self.lid = LocationIdentifier(f"{name}_{self.game_type}_{x}_{y}_{z}")
		self.no_connect = no_connect
		self.auto_connect = auto_connect
		self.portals = []
		# connections are f"on_axis_{x..z}" in a list for each axis
		self.is_map = is_map
		self.occupying = []
		self.connections = {}
		self.parent = parent
		self.x, self.y, self.z = x, y, z
		self.name = name
		self.hiding = {}
		self.in_location = {}
		self.items = items
		self.description = description
		self.threats = {}

	def setxyz(self, *xyz):
		self.x, self.y, self.z = xyz
		return self.getxyz()



	def getxyz(self):
		return (self.x, self.y, self.z)

class ScenarioWide(ScenarioLocation):
	pass 

class ScenarioTall(ScenarioLocation):
	pass

class ScenarioLong(ScenarioSpan):
	def __init__(self, parent, name, yrange, xz, **kwargs):
		super().__init__(parent, name, **kwargs):

class ScenarioSpan(ScenarioLocation):
	def __init__(self, parent, name, longaxis, otheraxises, **kwargs):
		self.parent.insert()

class ScenarioPortal(ScenarioLocation):
	def __init__(self, parent, name="", **kwargs):
		self.first, self.second = self.between = kwargs.get("between")
		self.lid = f"portal_{self.first}"
		self.exit = True 
		self.enter = True
		px, py, pz = parent.getxyz()
		self.lid = f"{self.name}from_{px}{py}{pz}_to"
		self.link = True


smap = ScenarioMap("Haunted Mansion", start=(0, 0, 0))
smap.install(ScenarioExterior("1951 Palemra Steet")



		
