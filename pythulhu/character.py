import json
from refs import *
from pprint import pprint
import random
from pathlib import Path
import pickle
from skills import getslots
from dataparse import *
#import weapons
from uuid import uuid4

random.seed()

_primary = ["pow", "str", "con", "dex", "app", "siz", "edu", "int"]
_secondary = ["mov", "db", "build", "hp", 
        "hp", "mp", "sanity", "max_sanity", "dodge"]
_rolled = ["pow", "str", "con", "dex", "app", "siz", "edu", "int", "dodge"]



class Character:
    def __init__(self, **kwargs):
        # characters can reliably be addressed by there cid in the charmap.
        self.keeper = None
        self.gametype = "NonPlayerCharacter"
        self.gameid = str(uuid4()) 
        self.skills = kwargs.get("skills", {})
        self.ownlanguage = kwargs.get("language", "English")
        self.skills = {}

    def skill_value(self, arg, skill=True):
        if skill is True:
            return attrget(self, "skills", arg, "value")
        else:
            return getattr(self, arg)
    #skills include characteristics
    def connect_to_keeper(self, keeper):
        return {"investigator": self, "request": "accept"}
    def getskill(self, skillname):
        return self.skills.get(skillname) or {"name": skillname, "value": self.__dict__.get(skillname, 0)}

    def improvement_check(self, key, count=1):
        val = getattr(self, key)
        for x in range(0, count):
            if val < random.randrange(1, 100):
                 val += random.randrange(1, 10)
        setattr(self, key, val)

    def getchars(self, primary=True, secondary=False, result={}):
        if primary is True:
            result = self.primary()
        if secondary is True:
            result = {**self.result, **self.secondary()}
        else:
            result = self.__dict__
        return result

    def skillroll(self, skill=None, oppskill=None, challenge=REGULAR, bonus=0, penalty=0,):
        skill = self.getskill(skill)
        return skillroll(skill=skill, challenge=challenge, bonus=bonus, penalty=penalty) if not oppskill else opposed_skillroll(
                skill, oppskill, bonus=bonus, penalty=penalty)

    def primary(self, result={}):
        return {k: getattr(self, k) for k in _primary}

    def secondary(self, result={}):
        return {k: getattr(self, k) for k in _secondary}

    def purchase(item, ptype="item", cash=False):
        cost, key, data = items.purchase_item(item, ptype)
        if cash is True:
            self.cash -= cost

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
        slotdefs = getslots()
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

    def to_pdf(self, template=topdftemp, result={}):
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

    def to_json(self, template=tojsontemp):
        for k, v in self.__dict__.items():
            if k in template:
                template[k] = v
        return template

    def to_prism(self, template=toprismtemp):
        pass 

    def pass_data(self, key, location):
        self.post(getattr(self, attr), location)

    def post(self, value, location):
        pass 

class Investigator(Character):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gametype = "Investigator"
        #self.pdf = kwargs.get("pdf", topdftemp.items())
        #self.prism = kwargs.get("prism", toprism.items())
        #self.json = kwargs.get("json", tojson.items())
        for k, v in kwargs.items():
            if k in tojsontemp.keys():
                setattr(self, k, v)

def save(investigator, path):
    path = Path(path)
    if not path.exists():
        path.touch()
    path.write_bytes(pickle.dumps(investigator))

def open(path):
    path = Path(path)
    if path.exists():
        return pickle.loads(path.read_bytes())

