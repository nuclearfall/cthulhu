from pprint import pprint
from pathlib import Path
from uuid import uuid4
import pickle
import json
from typing import TypedDict
import refs
import uuid 
import npc

def rget(d, *args, default={}):
	if not args:
		return d or default
	else:
		key, *args = args 
		return rget(d.get(key), *args, default=default)

def load(path):
	path = Path(path)
	if path.suffix == ".json":
		with open(path, "r") as fp:
			return json.load(fp)
	else:
		with open(path, "rb") as fp:
			return pickle.load(fp)

def dump(data, path):
	path = Path(path)
	if path.suffix == ".json":
		with open(path, "w") as fp:
			return json.dump(data, fp, indent=4)
	else:
		with open(path, "wb") as fp:
			return pickle.dump(data, fp)

class GameStack:
	def __init__(self, *args):
		self.stack = []
		if args:
			[self.push(*args)]
	def __str__(self):
		return str(self.stack)
	def push(self, *gameobjects):
		for obj in gameobjects:
			self.stack.append(obj)
		return self.stack
	def pop(self, arg=None):
		if arg:
			return self.stack.pop(arg)
		else:
			return self.stack.pop()
	def index(self, obj):
		return self.stack.index(obj)
	def first(self):
		if self.stack:
			return self.stack[0]
		else:
			return None
	def rest(self):
		x, *stack = self.stack 
		return stack
	def cat(self, lsorstack):
		if isinstance(lsorstack, list):
			self.stack += ls
		else:
			self.stack += lsorstack.stack
		return self.stack

class GameObject:
	def __init__(self, **kwargs):
		self.key = str(uuid4())
		self.name = ""
		self.visible = True
		self.description = ""
		self.brief = ""
		self._gsstack = GameStack()
		self.stack = self._gsstack.stack
		self.location = None
		self.interactions = None
		self.state = None
		self.sets(**kwargs)

	def get(self, key, default=0):
		return self.__dict__.get(key, default)

	def gets(self, *keys):
		return [self.get(key, 0) for key in keys]

	def rget(self, *keys):
		rget(self.__dict__, *keys)

	def sets(self, **kwargs):
		for k, v in kwargs.items():
			setattr(self, k, v)

	def load(self, path):
		path = Path(path)
		if path.suffix == ".json":
			with open(path, "r") as fp:
				self.sets(**json.load(fp))
		else:
			with open(path, "rb") as fp:
				self.sets(**pickle.load(fp))
	def loads(self, data):
		self.sets(**data)
		return self.__dict__

	def dump(self, path):
		path = Path(path)
		if path.suffix == ".json":
			with open(path, "w") as fp:
				return json.dump(self.dumps(), fp, indent=4)
		else:
			with open(path, "wb") as fp:
				return pickle.dump(self, fp)

	def dumps(self, exclude=["_gsstack"]):
		return {k:v for k, v in self.__dict__.items() if k not in exclude}


class GameMap(GameObject):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

class GameScene(GameMap):
	pass

class GameEntity(GameObject):
	pass

class GameCharacter(GameEntity):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		if not kwargs:
			self.loads(npc.chargen())
		if kwargs.get("random", None) is True:
			self.loads(npc.chargen(**kwargs))
		self.charsum = self.charsummary()
		self.skillsum = self.skillsummary()
		self.infosum = self.info()

	def info(self):
		return [f"{self.name:60}", f"{self.age} year old {self.occupation:42}"]
	def charsummary(self, ctypes={"primary": ["pow", "str", "con", "dex", "app", "siz", "edu", "int"],
				"secondary": ["luck", "mov", "db", "build", "hp", "mp", "sanity"]}):
		primchars = ctypes.get("primary")
		secondchars = ctypes.get("secondary")
		chars = primchars + secondchars
		vals = self.gets(*chars)
		lines = []
		string = f""
		for i, (k, v) in enumerate(dict(zip(chars, vals)).items()):
			if i % 5 == 0 or i == len(chars):
				lines.append(string)
				string = f""
				string += f"{k:7}: {v:>3}  "
			else:
				string += f"{k:7}: {v:>3}  "

		lines.append(string)
		return lines[1:]

	def skillsummary(self):
		lines = []
		line = f""
		for i, (k, v) in enumerate(self.get("skills").items()):
			ischecked = " - " if k in ["Cthulhu Mythos", "Credit Rating"] else "[X]" if v.get("checked") is True else "[ ]"
			if i % 2 == 0 or i == len(self.get("skills")):
				lines.append(line)
				line = f"" 	
			line += f"{ischecked} {k:23}: {v.get('value'):3}   "
			
		return lines[1:]
	def dodgechar(self):
		self.rget("skills", "Dodge")

		

path = "char.pkl"
char = GameCharacter(name="George", random=True)
#print(char.skills)

[pprint(GameCharacter(random=True).gets("infosum", "charsum", "skillsum")) for i in range(0, 1000)]



		