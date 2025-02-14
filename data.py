from scenes.simulation.house import House


class Data:
    def __init__(self):
        # Town
        self.stability = 75
        self.people = 100
        self.buffs = []
        self.debuffs = []
        self.houses = [House('small_house', 200, 200),
                       House('small_house', 500, 300)]
        self.schools = 0
        self.guard_houses = 0
        self.hospitals = 0
        self.price_multiplier = 1

        # Town development
        self.education = 50
        self.safety = 50
        self.health = 50

        # Resources
        self.resource_types = ['Food', 'Water', 'Wood', 'Stone']
        self.food = 800
        self.water = 2000
        self.wood = 0
        self.stone = 0

        # Resources storage
        self.food_storage = 1000
        self.water_storage = 2500

        # Player stats
        self.wood_click_value = 1
        self.stone_click_value = 1
        self.food_click_value = 5
        self.water_click_value = 2

        # Workers
        self.workers = 0
        self.lumberjacks = 0
        self.miners = 0
        self.hunters = 0

        # Upgrade costs
        self.upgrade_wood_click_value_cost = 50
        self.upgrade_stone_click_value_cost = 100

        # Hire costs
        self.hire_lumberjack_cost = 300
        self.hire_miner_cost = 500
        self.hire_hunter_cost = 100

    def to_dict(self):
        return {
        "stability": self.stability,
        "people": self.people,
        "buffs": self.buffs,
        "debuffs": self.debuffs,
        "houses": [house.to_dict() for house in self.houses],
        "schools": self.schools,
        "guard_houses": self.guard_houses,
        "hospitals": self.hospitals,
        "price_multiplier": self.price_multiplier,
        "education": self.education,
        "safety": self.safety,
        "health": self.health,
        "resource_types": self.resource_types,
        "food": self.food,
        "water": self.water,
        "wood": self.wood,
        "stone": self.stone,
        "food_storage": self.food_storage,
        "water_storage": self.water_storage,
        "wood_click_value": self.wood_click_value,
        "stone_click_value": self.stone_click_value,
        "food_click_value": self.food_click_value,
        "water_click_value": self.water_click_value,
        "workers": self.workers,
        "lumberjacks": self.lumberjacks,
        "miners": self.miners,
        "hunters": self.hunters,
        "upgrade_wood_click_value_cost": self.upgrade_wood_click_value_cost,
        "upgrade_stone_click_value_cost": self.upgrade_stone_click_value_cost,
        "hire_lumberjack_cost": self.hire_lumberjack_cost,
        "hire_miner_cost": self.hire_miner_cost,
        "hire_hunter_cost": self.hire_hunter_cost
        }
    