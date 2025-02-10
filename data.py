from scenes.simulation.house import House


class Data:
    def __init__(self):
        # Town
        self.stability = 75
        self.people = 100
        self.houses = [House('small_house', 200, 200),
                       House('small_house', 500, 300)]
        self.schools = 0

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
