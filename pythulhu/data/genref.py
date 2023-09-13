{
"agemods": 
{
	range(15, 20):
	{
		"penalties": 
		[
			[-5, "str", "siz"],
			[-5, "edu"]
		]
	},
	range(20,40): 
	{
		improvement_check: 1
	},
	range(40,50): 
	{
		"penalties": 
		[
			[-5, "str", "dex", "con"],
			[-5, "app"],
			[-1, "mov"]
		],
		improvement_check: 2
	},
	range(50, 60): 
	{
		"penalties": 
		[
			[-10, "str", "dex", "con"],
			[-10, "app"],
			[-2, "mov"]
		],
		improvement_check: 3
	},
	range(60,70): 
	{
		"penalties": 
		[
			[-20, "str", "dex", "con"],
			[-15, "app"],
			[-3, "mov"]
		],
		improvement_check: 4
	},
	range(70,80): 
	{
		outofprime_appadj
		improvement_check
	},
	range(80,100): 
	{
		outofprime_appadj: -25,
		"penalties": 
		[
			[-80, ["str", "dex", "con"]],
			[-25, "app"],
			[-5, "mov"]
		],
		improvement_check: 4
	}
},
	"buildanddb": 
	[
		{
			"highValue": 64,
			"lowValue": 2,
			"DamageBonus": "-2",
			"Build": -2
		},
		{
			"highValue": 84,
			"lowValue": 64,
			"DamageBonus": "-1",
			"Build": -1
		},
		{
			"highValue": 124,
			"lowValue": 85,
			"DamageBonus": "0",
			"Build": 0
		},
		{
			"highValue": 164,
			"lowValue": 125,
			"DamageBonus": "1d4",
			"Build": 1
		},
		{
			"highValue": 204,
			"lowValue": 165,
			"DamageBonus": "1d6",
			"Build": 2
		}
	],
	"Wealth": {
		"0-0": {
			"name": "Penniless",
			"Cash": 0.5,
			"Assets": 0,
			"SpendingLevelVal": 0.5
		},
		"1-10": {
			"name": "Poor",
			"CashMult": 1,
			"AssetMult": 1,
			"SpendingLevel": 250
		},
		"10-50": {
			"name": "Average",
			"CashMult": 2,
			"AssetMult": 50,
			"SpendingLevel": 250
		},
		"50-90": {
			"name": "Wealthy",
			"CashMult": 5,
			"AssetMult": 500,
			"SpendingLevel": 250
		},
		"90-99": {
			"name": "Rich",
			"CashMult": 20,
			"AssetMult": 2000,
			"SpendingLevel": 250
		},
		"99-100": {
			"name": "Super Rich",
			"Cash": 50000,
			"Assets": 50000000,
			"SpendingLevel": 5000
		}
	},
	"ExperiencePackages": {
		"Soldier": {
			"package": "War Experience",
			"sanity_loss": "1d10+5",
			"value": 70,
			"selections": [
				"Climb", 
				"Brawl",
				"Rifle/Shotgun",
				"First Aid",
				"Intimidate",
				"Listen",
				"Stealth",
				"Throw",
				"Sleight of Hand",
				"Spot Hidden",
				"Survival"
			],
			"trauma": [
				["phobia_manias", "injury_scars"]
			],
			"notes": "Immune to sanity losses resulting from viewing a corpse or gross injury." 
		},
		"Officer": {
			"package": "War Experience",
			"sanity_loss": "1d10 + 5",
			"value": 70,
			"selections": [
				"Climb", 
				"Handgun",
				"First Aid",
				"Intimidate",
				"Listen",
				"Navigate",
				[1, "interpersonal"],
				"Stealth",
				"Spot Hidden"
			],
			"trauma": [
				["phobia_manias", "injury_scars"]
			],
			"notes": "Immune to sanity losses resulting from viewing a corpse or gross injury." 
		},
		"Police": {
			"package": "Police Experience",
			"age": 25,
			"sanity_loss": "1d10",
			"value": 60,
			"selections": [
				["interpersonal"],
				["Handgun", "Rifle/Shotgun"],
				["languages"]
			],
			"skills": [
				"Climb",
				"Drive Auto",
				"Brawl", 
				"First Aid",
				"Intimidate",
				"Law",
				"Listen",
				"Track"
			],
			"trauma": [
				["phobia_manias", "injury_scars"]
			],
			"notes": "Immune to sanity losses resulting from viewing a corpse." 
		},
		"Crime": {
			"package": "Organized Crime Experience",
			"age": 20,
			"sanity_loss": "1d10",
			"value": 60,
			"selections": [
				["fighting"],
				["firearms"],
				["interpersonal"]
			],
			"skills": [
				"Climb",
				"Drive Auto",
				"Locksmith",
				"Law",
				"Listen",
				"Psychology",
				"Sleight of Hand",
				"Spot Hidden"		
			],
			"trauma": [
				["phobia_manias", "injury_scars"]
			],
			"notes": "Immune to sanity losses resulting from viewing a corpse, witnessing or performing a murder, or seeing violence perpetrated against a human being." 
		},
		"Medical": {
			"package": "Medical Experience",
			"age": 30,
			"value": 60,
			"selections": [
				["science"],
				["science"]
			],
			"skills": [
				"First Aid",
				"Law",
				"Listen",
				"Medicine",
				"Psychology",
				"Spot Hidden"
			],
			"trauma": [
				["phobia_manias"]
			],
			"notes": "Immune to sanity losses resulting from viewing a corpse or gross injury." 
		},
		"Sceptic": {
			"package": "Mythos Experience",
			"value": "1d10 + 5",
			"sanity_loss": "1d10 + 5",
			"exception": true,
			"skills": [
				"Cthulhu Mythos"
			],
			"trauma": [
				["phobia_manias", "injury_scars", "strange_encounters"],
				["phobia_manias", "injury_scars", "strange_encounters"]
			],
			"spells": false,
			"notes": "" 
		},
		"Believer": {
			"package": "Mythos Experience",
			"exception": true,
			"skills": [
				"Cthulhu Mythos"
			],
			"trauma": [
				["phobia_manias", "injury_scars", "strange_encounters"],
				["phobia_manias", "injury_scars", "strange_encounters"]
			],
			"spells": true,
			"notes": "" 
		}
	}
}