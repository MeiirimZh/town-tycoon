import json
import os

import pygame.font

from config import MONOCRAFT_FONT
from data import Data
from scenes.simulation.house import House


def get_quarter(x, y):
    quarter_size = y / 4
    if x == 0:
        return 1
    for i in range(4):
        if i * quarter_size < x <= (i + 1) * quarter_size:
            return i + 1


def get_section(x, y, z):
    section_size = y / z
    if x == 0:
        return 1
    for i in range(z):
        if i * section_size < x <= (i + 1) * section_size:
            return i + 1


def create_font(size):
    return pygame.font.Font(MONOCRAFT_FONT, size)

def save(data):
    with open("data.json", "w") as f:
        json.dump(data.to_dict(), f, indent=4)

def load_houses():
    with open("data.json", "r") as f:
        data_dict = json.load(f)
    houses = []
    for house in data_dict["houses"]:
        houses.append(House(house["house_type"], house["x"], house["y"]))
    
    return houses

def load():
    if not os.path.exists("data.json") or os.stat("data.json").st_size == 0:
        data = Data()
        save(data)
        return data

    with open("data.json", "r") as f:
        try:
            data_dict = json.load(f)
        except json.JSONDecodeError:
            data = Data()
            save(data)
            return data
        
        data = Data()

        data.stability = data_dict["stability"]
        data.people = data_dict["people"]
        data.buffs = data_dict["buffs"]
        data.debuffs = data_dict["debuffs"]
        data.houses = load_houses()
        data.schools = data_dict["schools"]
        data.guard_houses = data_dict["guard_houses"]
        data.hospitals = data_dict["hospitals"]
        data.price_multiplier = data_dict["price_multiplier"]
        data.education = data_dict["education"]
        data.safety = data_dict["safety"]
        data.health = data_dict["health"]
        data.resource_types = ['Food', 'Water', 'Wood', 'Stone']
        data.food = data_dict["food"]
        data.water = data_dict["water"]
        data.wood = data_dict["wood"]
        data.stone = data_dict["stone"]
        data.food_storage = data_dict["food_storage"]
        data.water_storage = data_dict["water_storage"]
        data.wood_click_value = data_dict["wood_click_value"]
        data.stone_click_value = data_dict["stone_click_value"]
        data.food_click_value = data_dict["food_click_value"]
        data.water_click_value = data_dict["water_click_value"]
        data.workers = data_dict["workers"]
        data.lumberjacks = data_dict["lumberjacks"]
        data.miners = data_dict["miners"]
        data.hunters = data_dict["hunters"]
        data.upgrade_wood_click_value_cost = data_dict["upgrade_wood_click_value_cost"]
        data.upgrade_stone_click_value_cost = data_dict["upgrade_stone_click_value_cost"]
        data.hire_lumberjack_cost = data_dict["hire_lumberjack_cost"]
        data.hire_miner_cost = data_dict["hire_miner_cost"]
        data.hire_hunter_cost = data_dict["hire_hunter_cost"]

    return data