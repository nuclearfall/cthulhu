import json
from pprint import pprint
import random
from pathlib import Path
import pickle
import skills as skl
with open("../data/character.json") as fp:
    _character_def = json.load(fp)

with open("../data/investigator.json") as fp:
    template = json.load(fp)

_primary = ["pow", "str", "con", "dex", "app", "siz", "edu", "int"]
_secondary = ["mov", "db", "build", "hp", 
        "hp", "mp", "sanity", "max_sanity", "dodge"]
_rolled = ["pow", "str", "con", "dex", "app", "siz", "edu", "int", "dodge"]
class Investigator:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        if not kwargs.get("skills"):
            self.skills = {}
        self.pdf = {}
        if not kwargs.get("language"):
            self.ownlanguage = "English"

    def improvement_check(self, key, count=1):
        val = getattr(self, key)
        for x in range(0, count):
            if val < random.randrange(1, 100):
                 val += random.randrange(1, 10)
        setattr(self, key, val)

    def getchars(self, typeof=["primary"], result={}):
        if "primary" in typeof:
            result = self.primary()
        if "secondary" in typeof:
            result = {**self.result, **self.secondary()}
        return result

    def primary(self, result={}):
        for key in _primary:
            result[key] = getattr(self, key)
        return result

    def secondary(self, result={}):
        for key in _secondary:
            result[key] = getattr(self, key)
        return result

    def update_character(self, **kwargs):
        for key, val in kwargs:
            setattr(self, key, val)

    def wealth(self):
        credit = self.investigator.skills.get("Credit Rating")
        
    def pdfset_values(self, key, value):
        self.pdf[key] = value
        self.pdf[key+"_half"] = int(value/2)
        self.pdf[key+"_fifth"] = int(value/5)
        self.pdf[key+"_Chk"] = ""

    # Likely a fair bit of extra cruftiness in these pdf export methods.
    def pdfset_skill(self, tkeys):
        self.pdf = {}
        slotdefs = skl.get_slots()
        #skills that only exist on the sheet:
        # Set Own Language Skill off the bat:
        self.pdf["SkillDef_OwnLanguage"] = self.language
        self.pdfset_values("Skill_OwnLanguage", self.skills.get("Own Language").get("value"))

        pdf_children = [sn for sn in slotdefs]
        # Filter out custom and special fields f        
        tdefs = [k for k in tkeys if k.startswith("SkillDef") and not "OwnLanguage" in k]
        other_tskills = [k for k in tkeys if k not in tdefs and not k.endswith(
                "_fifth") and not k.endswith("_half") and not k.endswith("_Chk") and not "OwnLanuage" in k]

        for skill in self.skills.values():
            if not skill:
                pass
            value = skill.get("value")
            pdfslot = skill.get("pdfslot")
            skname = skill.get("name")
            if skname == "Brawl":
                self.pdfset_values("Skill_Fighting", value)
            elif pdfslot in pdf_children:
                if pdfslot == "Custom" or not slotdefs[pdfslot]:
                    num = slotdefs["Custom"].pop(0)
                    self.pdf["SkillDef_Custom"+num] = skname
                    self.pdfset_values("Skill_Custom"+num, value)
                else:
                    num = slotdefs[pdfslot].pop(0)
                    self.pdf["SkillDef_"+pdfslot+num] = skname 
                    self.pdfset_values("Skill_"+pdfslot+num, value)
            elif pdfslot:
                self.pdfset_values("Skill_"+pdfslot, value)
        return None

    def pdfexport(self, template=template, result={}):
        self.dodge = self.skills.get("Dodge").get("value")
        self.pdf = template
        skill_keys = [k for k in template.keys() if k.startswith("Skill")]
        nonskills = {k:v for k, v in template.items() if k not in skill_keys and not k.endswith("_half") and not k.endswith("_fifth")}
        self.pdfset_skill(skill_keys)
        for tkey, tk in nonskills.items():
            value = self.__dict__.get(tk)
            # include Brawl challenge difficulties as an exception in Weapons.
            if tkey.startswith("Weapon"):
                if tkey == "Weapon_Regular0":
                    print("match")
                    self.pdf["Weapon_Regular0"] = self.skills.get("Brawl").get("value")
                    self.pdf["Weapon_Hard0"] = int(self.skills.get("Brawl").get("value") / 2)
                    self.pdf["Weapon_Extreme0"] = int(self.skills.get("Brawl").get("value") / 5)
            elif value and tk in _rolled:
                self.pdfset_values(tkey, value)
            elif value is not None and tk == "dodge":
                self.pdf[tkey] = self.get_dodge()
            elif value is not None:
                self.pdf[tkey] = value
            else:
                self.pdf[tkey] = ""
        return self.pdf


    def get_skillindex(self, name):
        for index, (skname, _) in enumerate(self.investigator.skills):
            if skname == name:
                return index
        return None

def save(investigator, path):
    path = Path(path)
    if not path.exists():
        path.touch()
    path.write_bytes(pickle.dumps(investigator))

def open(path):
    path = Path(path)
    if path.exists():
        return pickle.loads(path.read_bytes())

