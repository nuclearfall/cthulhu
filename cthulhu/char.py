import logging
import json
import random
from pathlib import Path
from pprint import pprint
from functools import reduce
# from cthulhu.skill import skill
# from cthulhu.weapon import weapon, firearm
# from cthulhu.roll import result



def load_json_files(paths):
    json_list = []
    for path in paths:
        print(path)
        with open(path, 'r') as fp:
            json_list.append(json.load(fp))
    return json_list


# Rolled Stats
# def roll_stats(character, reference):
#     stat_dice = reference.get("statDice")
#     stats = character.get("stats")
#     for key in stat_dice:
#         roll = stat_dice.get(key)
#         if roll == 3:
#             if key == "luck":
#                 character["luck"] = random.randrange(3,19)*5
#             else:
#                 stats[key] = random.randrange(3,19)*5
#         elif roll == 2:
#             stats[key] = random.randrange(2,13)*5+6
#     return character


# # Secondary Stats
# def set_secondary_stats(character, reference):
#     bd_build_chart = reference.get("damageBonusAndBuildChart")
#     stats = character.get("stats")
#     strength = stats.get("strength")
#     cons = stats.get("constitution")
#     size = stats.get("size")
#     dex = stats.get("dexterity")
#     intel = stats.get("intelligence")
#     power = stats.get("power")
#     db, bld = db_and_build(character, reference)
#     character["maxHitpoints"] = character["currentHitpoints"] = int((cons + size) / 10)
#     character['damageBonus'] = db 
#     character['build'] = bld
#     character["maxSanity"] = character["currentSanity"] = power
#     character['currentMagicPoints'] = character["maxMagicPoints"] = int(power / 5)
#     character['idea'] = intel 
#     character['dodge'] = int(dex / 2)
#     return character

# def db_and_build(character, reference):
#     reference.get("damageBonusAndBuildChart")
#     db_build_list = reference.get("damageBonusAndBuildChart")
#     stats = character.get("stats")
#     str_siz = stats.get("size") + stats.get("strength")
#     for comp in db_build_list:
#         if comp.get("lowValue") <= str_siz <= comp.get("highValue"):
#             db = comp.get("damageBonus")
#             bld = comp.get("build")
#             return (db, bld)

# def improvement_check(value, num_check):
#     if num_check:
#         rolls = [random.randrange(0, 101) for r in range(num_check)]
#         successes = [roll for roll in rolls if roll > value]
#         improves = reduce(lambda x, y: x if x > y else y, rolls)
#         for success in successes:
#             value += random.randrange(1, 11)
#     return value

# def movement_rate(character):
#     stats = character.get("stats")
#     strength = stats.get("strength")
#     dexterity = stats.get("dexterity")
#     size = stats.get("size")
#     if strength > size and dexterity > size:
#         return 9
#     elif strength > size or dexterity > size or (dexterity == size == strength):
#         return 8
#     else:
#         return 7


# ### Age Modifications
# def get_agemods(char, reference):
#     agechart = reference.get("ageModifiers")
#     age = char.get("age")
#     for agemod in agechart:
#         if agechart[agemod].get("ageLow") <= age <= agechart[agemod].get("ageHigh"):
#             return agechart[agemod]

# def penalty_total(choices):
#     return sum(choices.values())

# def penalty_from_stat(character, from_stat, value):
#     stats = character.get("stats")
#     stat = character.get("stats").get(from_stat) + value
#     return stat

# def penalties_among_stats(character, value, amongstats, choices):
#     stats = character.get("stats")
#     if value == penalty_total(choices):
#         for astat in amongstats:
#             choice_value = choices.get(astat, 0)
#             if stats.get(astat) + choice_value < 0:
#                 logging.error("ERROR: value would make characteristic less than zero.")
#             else:
#                 stats[astat] += choice_value
#     else:
#         logging.error("ERROR: values don't equal required penalty total.")
#     return stats

# def age_adjust(character, reference, choices):
#     stats = character.get("stats")
#     agemods = get_agemods(character, reference)
#     penalties = agemods.get("createPenalties")
#     ed_rolls = agemods.get("educationChecks")
#     movement_penalty = 0
#     for penalty in penalties:
#         fromstat = penalty.get("from")
#         amongstats = penalty.get("among")
#         value = penalty.get('value')
#         if fromstat == "movement":
#             movement_penalty = value
#         elif fromstat:
#             print(fromstat)
#             character["stats"][fromstat] = penalty_from_stat(character, fromstat, value)
#         if amongstats:
#             character["stats"] = penalties_among_stats(character, value, amongstats, choices)
#     print(movement_penalty)
#     print(movement_rate(character))
#     character["movement"] = movement_rate(character) + movement_penalty
#     print(character["movement"])
#     if ed_rolls:
#         ed_value = stats.get("education")
#         character['stats']["education"] = improvement_check(ed_value, ed_rolls)
#     return character


# # Occupation Setting
# def get_base_skill_value(char_skill, skills):
#     cspec = char_skill.get("specailty")
#     cname = char_skill.get("name")
#     for skill in skills:
#         spec = skill.get("specailty")
#         name = skill.get("name")
#         base = skill.get("base")
#         if spec and spec == cspec and name == cname:
#             char_skill["base"] = base 
#         elif name and name == cname:
#             char_skill["base"] = base
#     return char_skill

# def list_occupations(occupations):
#     occupations = occupations.get('occupations')
#     occ_list = [occ.get('name') for occ in occupations]
#     return occ_list

# def get_occupation(occupation, occupations):
#     occ_list = list_occupations(occupations)
#     for occ in occupations.get("occupations"):
#         name = occ.get("name")
#         if name == occupation:
#             return name
#     else:
#         return None

# def get_skill_list(skills):
#     skill_list = skills.get("skills")
#     return [sk for sk in skill_list]

# def occ_skill_choice_list(occ_skill, skills):
#     selection = skill.get("selection")
#     numselect = skill.get("numSelect")
#     if selection == []:
#         return (numselect, get_skill_list(skills))
#     elif selection:
#         seectable_skills = [get_base(sel_skill, skills) for sk in selection]
#         return (numselect, selectable_skills)


def init_character(character, references, occupations, **kwargs):
    for key in kwargs:
        if key == "occupation":
            pass
        else:
            character[key] = kwargs[key]
    occupation = get_occupation(kwargs.get("occupation"), occupations)
    if occupation is not None:
        character["occupation"] = occupation
        character = roll_stats(character, references)
        return character
    else: 
        return logging.error("Error: Not a valid occupation.")



    # temp = character_gen(template=template, occupations=occupations)

class Character:
    def __init__(self, sheet, reference, occupations, 
            skills=None, weapons=None, spells=None, **kwargs):
        # self.character = character 
        self.reference = reference
        self.occupations = occupations
        self.skills = skills 
        self.weapons = weapons
        self.spells = spells
        self.stats = sheet.get("stats")
        self.isAged = False
        for key in kwargs:
            if key in sheet.keys():
                if key == "stats":
                    pass
                if key == "occupations" and kwargs[key] not in self.list_occupations():
                    logging.error(f"Error: {kwargs[key]} is not a valid occupation.")
                else:
                    setattr(self, key, kwargs[key])
            else:
                logging.error(f"Error: {key} is not a field.")

    def list_occupations(self):
        occupations = self.occupations.get('occupations')
        occ_list = [occ.get('name') for occ in occupations]
        return occ_list

    def set_primary(self):
        stat_dice = self.reference.get("statDice")
        for key in stat_dice:
            roll = stat_dice.get(key)
            if roll == 3:
                if key == "luck":
                    self.luck = random.randrange(3,19)*5
                else:
                    self.stats[key] = random.randrange(3,19)*5
            elif roll == 2:
                self.stats[key] = random.randrange(2,13)*5+6

    def modify_by_age(self):
        stats = self.stats
        agemods = self.get_agemods()
        penalties = agemods.get("createPenalties")
        ed_rolls = agemods.get("educationChecks")
        movement_penalty = 0
        for penalty in penalties:
            fromstat = penalty.get("from")
            amongstats = penalty.get("among")
            value = penalty.get('value')
            if fromstat == "movement":
                movement_penalty = value
            elif fromstat:
                print(fromstat)
                print(stats)
                self.stats[fromstat] += value
            if amongstats:
                self.stats = self.penalties_among_stats(value, amongstats, choices)

        self.movement = self.movement_rate(character) + movement_penalty
        if ed_rolls:
            ed_value = stats.get("education")
            stats["education"] = improvement_check(ed_value, ed_rolls)
        self.isAge = True

    def get_agemods(self):
        agechart = self.reference.get("ageModifiers")
        for agemod in agechart:
            if agechart[agemod].get("ageLow") <= self.age <= agechart[agemod].get("ageHigh"):
                return agechart[agemod]

    def penalty_total(self, choices):
        return sum(choices.values())

    # def penalty_from_stat(self, value, from_stat):
    #     return self.stats.get(from_stat) + value

    def penalties_among_stats(self, value, amongstats):
        choices = self.age_adjustments
        stats = self.stats
        if value == self.penalty_total(choices):
            for astat in amongstats:
                choice_value = choices.get(astat, 0)
                if stats.get(astat) + choice_value < 0:
                    logging.error("ERROR: value would make characteristic less than zero.")
                    raise ValueError
                else:
                    logging.debug(f"User removed {-choice_value} from {astat}")
                    stats[astat] += choice_value
        else:
            logging.error("ERROR: values don't equal required penalty total.")

    def set_secondary_stats(self):
        if isAged is True:
            bd_build_chart = self.reference.get("damageBonusAndBuildChart")
            stats = self.get("stats")
            self.damageBonus, self.build = db_and_build()
            self.maxHitpoints = self.currentHitpoints = int(
                (stats.get("constitution") + stats.get("size")) / 10)
            self.maxSanity = self.currentSanity = stats.get("power")
            self.currentMagicPoints = self.maxMagicPoints = int(stats.get("power") / 5)
            self.idea = stats.get("intelligence")
            self.dodge = int(stats.get("dexterity") / 2)
        else:
            logging.error("ERROR: Character has not been aged. Submit aging choices first.")

    def db_and_build(self):
        db_build_list = self.reference.get("damageBonusAndBuildChart")
        stats = self.stats
        str_siz = stats.get("size") + stats.get("strength")
        for comp in db_build_list:
            if comp.get("lowValue") <= str_siz <= comp.get("highValue"):
                db = comp.get("damageBonus")
                bld = comp.get("build")
                return (db, bld)

    def occupation_details(self):
        for occ in self.occuapations.get("occupations"):
            if occ.get("name") == self.occupation:
                return occ 

    def occupation_skills(self):
        skills = self.occupation_details().get("skillSelection")
        return [s.get("free") for free in 

    def list_skills(self):
        return [skill.get("name") for skill in self.skilldict.get("skills")]

    def list_nested_skills(self, nest):
        return [s.get('name') for free.get("free") in nest for s in free]

    def list_skill_options(self, nested_skills):
        if not nested_skills.get("selections"):
            return self.skill_names()
        else:
            return [skill.get("free").get("name") in nested_skills]

    def flatten_skills(self, skills, nest):
        # choices = self.occ_skill_choices
        for skill in enumerate(skills):
            decisions = skill.get("selections")
            if skill.get("numSelect") == len(decisions)
                skills = skills + self.nested_skills(nest) if len(nest) > 0 else []
                del(decisions)
        return skills

    def get_scenarios(self):
        return self.occupation_details().get('skillPointScenarios')

    def occupation_skill_points(self, scenario: int):
        points = 0
        skills = self.get_scenarios()[scenario]
        for k, v in skill,items():
            points += self.stats.get(k) * v
        return points

    def hobby_skill_points():
        pass

    def min_credit(self):
        return occ_data = self.get_occupation().get('lowCreditRating')
    def max_credit(self):
        return occ_data = self.get_occupation().get('HighCreditRating')

    def base_skills_from_occupation(self, decisions=None):
        named_skills = []
        decision_required = []
        for free in self.occupations.get("skillSelection"):
            skill = free.get("name")
            if name is not None:
                skills.append(skill_name)
            else:
                self.skill_select(free, decisions)
        named_skills += self.occupation_skill_select(self, decision_required, decisions)
        self.skils = named_skills

    def occupation_skill_select(options, selections):
        if not options:
            self.skills = self.occupation_get_skills()

            req_num= required.get("numSelect")
            req_len = len(required.get("selections"))
            for decision in decisions:
                num = 0
                if len(decision) == sel_len and  

                    if requ

            for requirement in required:
                if selections != [] and decision in selections:

                if "selections" == []:


        [skill for skill in decisions if]
                if is_possible_decision(self, skill, decisions):
                    for skill in decisions()


def main(): 
    random.seed()
    srcpath = Path().home().joinpath('local', 'src', 'cthulhu', 'cthulhu')
    filenames = ['character', 'reference', 'occupations', 
            'skills', 'items', 'weapons', 'spells']
    filepaths = []
    for name in filenames:
        jsonfile = srcpath.joinpath(name).with_suffix('.json')
        filepaths.append(jsonfile)
    (sheet, reference, occupations,
            skills, items, weapons, spells) = load_json_files(filepaths)
    char = Character(sheet, reference, occupations, playerName="Gary", 
            name="George Shelstein", age=52, 
            occupation="Architect")
    char.set_primary()
    char.age_adjust({"strength": -8, "dexterity": -2})
    #char = age_adjust(character, reference, {"strength": -8, "dexterity": -2})
    #char = set_secondary_stats()
    char = {key:val for key, val in char.__dict__.items() if key != "skills"}
    pprint(char)



def generate_character(**kwargs):
    character = CharacterGenertor(kwargs)
    character.set_primary_stats()
    character.modify_by_age()
    character.set_secondary_stats()
    character.skills = charcter.occupation_skills_select()



if __name__ == "__main__":
    main()
# class being(object):
#     def __init__(self, name, HP=0, era = 'Classic'):
#         self.name = name
#         self.maxHP = self.HP = HP
#         self.era = era
#         self.db = 0
#         self.build = 0
#         self.mov = 8
#         self.luck = 0
#         self.san = self.maxSan = 0
#         self.mp = 0
#         self.numAttacks = 1
#         self.armor = 0
#         self.currentWeapon = None

#         self.status = dict()
#         self.status['fightback'] = True
#         self.characteristics = dict()
#         self.skills = dict()
#         self.weapons = dict()

#     def setCharacteristic(self, characteristic, value):
#         self.characteristics[characteristic] = skill(characteristic, value)

#     def setSkill(self, skillName, value):
#         self.skills[skillName] = skill(skillName, value)

#     def addWeapon(self, weaponName, skillName, damage, weaponType='non-impaling', db=False, mal=101, ammo=0, numAttacks=1):
#         if weaponType != 'firearm':
#             self.weapons[weaponName] = weapon(weaponName, skillName, damage, weaponType=weaponType,  db=db, mal=mal)
#         else:
#             self.weapons[weaponName] = firearm(weaponName, skillName, damage, weaponType=weaponType,  db=db, mal=mal, ammo=ammo, numAttacks=numAttacks)

#     def setDodge(self, value=0):
#         try:
#             self.skills['Dodge'] = skill('Dodge' , self.characteristics['dexterity'].half)
#         except:
#             log.error("ERROR: Unable to set Dodge.")

#     def outNumbered(self):
#         """ returns True if they have already responded """
#         try:
#             if self.status['combat_response'] > self.numAttacks:
#                 return True
#         except KeyError:
#             self.status['combat_response'] = 0
#             return False

#         return False

#     def jsondump(self):
#         return jsonpickle.encode(self)

#     def initiative_value(self):
#         """ Return the initiative value for this character based on their current weapon. """
#         if self.currentWeapon is not None and self.currentWeapon.weaponType == 'firearm':
#             init_value = self.characteristics['dexterity'].value + 50
#         else:
#             init_value = self.characteristics['dexterity'].value

#         logging.debug("Combat: {} init value is {}".format(self.name, init_value))

#         return init_value

#     def setCurrentWeapon(self):
#         """ Ask the user what their current weapon should be. """
#         chosen = False
#         wlist = list(self.weapons)
#         if len(wlist) == 1:
#             weapon = 0
#             chosen = True

#         while chosen is False:

#             for w in wlist:
#                 print '{}. {} {}'.format(wlist.index(w)+1, w, self.weapons[w].damage)
#             weapon = raw_input('\n{} must choose their weapon: '.format(self.name))

#             try:
#                 weapon = int(weapon)-1
#                 if 0 <= weapon <= len(wlist)-1:
#                     chosen = True
#             except:
#                 pass

#         self.currentWeapon = self.weapons[wlist[weapon]]

# class character(being):
#     def __init__(self, name=''):
#         being.__init__(self, name)
#         for characteristic in ['STR', 'dexterity', 'APP', 'constitution', 'power', 'intelligence', 'size', 'EDU']:
#             self.setCharacteristic(characteristic, 0)

#         # only characters should check for major wounds. Is this true? Need to verify.
#         self.majorWound = 0

#         self.addWeapon('Unarmed',  '1d3', 'Fighting (Brawl)', db=True)  # ADD DAMAGE BONUS

#     def setSecondary(self):
#         self.setHP()
#         self.setSAN()
#         self.setBuildAndDB()
#         self.setmovement()
#         self.setMP()
#         self.setDodge()

#     def setHP(self):
#         """ Sets the maximum HP and current HP based on constitution and size.
#              Modify self.HP directly if you need to subtract or add HP.
#         """
#         try:
#             self.maxHP = (self.characteristics['constitution'].value + self.characteristics['size'].value) / 10
#             self.HP = self.maxHP
#         except:
#             logging.error("ERROR: Missing constitution or size. Please add those before setting HP.")

#     def setBuildAndDB(self):
#         """ Sets the initial damage bonus and build based on STR and size. """
#         try:
#             combined = self.characteristics['STR'].value + self.characteristics['size'].value
#         except:
#             logging.error("ERROR: Missing STR or size. Please add before setting up DB and build.")
#             return

#         if 2 <= combined <= 64:
#             self.db = self.build = -2
#         elif 65 <= combined <= 84:
#             self.db = self.build = -1
#         elif 125 <= combined <= 164:
#             self.db = '1d4'
#             self.build = 1
#         elif combined >= 165:
#             self.db = '1d6'
#             self.build = 2

#     def setmovement(self):
#         """ Sets movement based on dexterity, STR and size. """
#         try:
#             if self.characteristics['STR'].value < self.characteristics['size'].value and \
#                self.characteristics['dexterity'].value < self.characteristics['size'].value:
#                    self.mov = 7
#             elif self.characteristics['STR'].value > self.characteristics['size'].value and \
#                    self.characteristics['dexterity'].value > self.characteristics['size'].value:
#                    self.mov = 9
#         except:
#             logging.error('ERROR: Cannot set movement. Missing STR, dexterity or size.')

#     def setSAN(self):
#         """ Sets the initial sanity. """
#         try:
#             self.san = self.characteristics['power'].value
#             self.maxSan = self.san
#         except:
#             logging.error('ERROR: Need power before we can set SAN.')

#     def setMP(self):
#         """ Sets the inital power."""
#         try:
#             self.mp = self.characteristics['power'].fifth
#         except:
#             logging.error('ERROR: Need power before we can set MP.')

#     def checkMajorWound(self, damage):
#         # check for major wound
#         if self.HP > 0 and damage >= (self.maxHP / 2):
#             logging.info('DAMAGE: {} suffered a major wound.'.format(self.name))
#             # make a constitution check
#             if self.characteristics['constitution'].check() < result.normal:
#                 logging.info('DAMAGE: {} failed their constitution check - falling unconscious and will die.'.format(self.name))
#                 self.HP = 0


#     def __str__(self):
#         outstr = "Name: {}\n".format(self.name)
#         outstr = outstr + "Era: {}\n".format(self.era)
#         outstr = outstr +  "HP: {}\tMax HP: {}\tMP: {}\n".format(self.HP, self.maxHP, self.mp)
#         outstr = outstr +  "San: {}\tMax SAN: {}\n".format(self.san, self.maxSan)
#         outstr = outstr +  'DB: {}\tBuild: {}\tmovement: {}\n'.format(self.db, self.build, self.mov)
#         outstr = outstr +  'Luck: {}\n\n'.format(self.luck)
#         outstr = outstr +  "Characteristics:\n"
#         for characteristic in self.characteristics:
#             outstr = outstr +  str(self.characteristics[characteristic]) + '\n'

#         outstr = outstr + "\nSkills:\n"
#         for skills in sorted(self.skills):
#             outstr = outstr +  str(self.skills[skills]) + '\n'

#         outstr = outstr + "\nWeapons:\n"
#         for weapon in sorted(self.weapons):
#             outstr = outstr +  str(self.weapons[weapon]) + '\n'

#         return outstr

# class monster(being):
#     def __init__(self, name=''):
#         being.__init__(self, name)
#         for characteristic in ['STR', 'dexterity', 'APP', 'constitution', 'power', 'intelligence', 'size', 'EDU']:
#             self.setCharacteristic(characteristic, 0)

#         self.sanLoss = '0/0'
#         self.majorWound = 0

#     def __str__(self):
#         outstr = "Name: {}\n".format(self.name)
#         outstr = outstr +  "HP: {}\tMax HP: {}\tMP: {}\n".format(self.HP, self.maxHP, self.mp)
#         outstr = outstr +  'DB: {}\tBuild: {}\tmovement: {}\n'.format(self.db, self.build, self.mov)
#         outstr = outstr + 'Armor: {}\tNumber of Attacks: {}\tSanity Loss: {}\n\n'.format(self.armor, self.numAttacks, self.sanLoss)
#         outstr = outstr +  "Characteristics:\n"
#         for characteristic in self.characteristics:
#             if self.characteristics[characteristic].value > 0:
#                 outstr = outstr +  str(self.characteristics[characteristic]) + '\n'

#         outstr = outstr + "\nSkills:\n"
#         for skills in sorted(self.skills):
#             outstr = outstr +  str(self.skills[skills]) + '\n'

#         outstr = outstr + "\nWeapons:\n"
#         for weapon in sorted(self.weapons):
#             outstr = outstr +  str(self.weapons[weapon]) + '\n'
#         return outstr

# def json_import(myjson):
#     """ Imports the char.jsondump() version of a char and returns the new object. """
#     return jsonpickle.decode(myjson)


