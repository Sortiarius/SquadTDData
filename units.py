import sqlite3, json, re
import xml.etree.ElementTree as ET

from utils import get_data_strings, get_weapon_type, rewrite_string


def get_unit_data(squad_data):
    unit_tree = ET.parse('data/UnitData.xml')

    unit_root = unit_tree.getroot()
    units = {}
    for child in unit_root:
        if child.attrib.get('parent') != 'SquadronUnitTemplate':
            continue

        curr_unit = {
            "name": squad_data["Names"][child.attrib['id']],
            "id": child.attrib['id'],
            "abilities": []
        }

        for subchild in child:
            if subchild.tag == 'LifeMax':
                curr_unit["life"] = subchild.attrib['value']
            elif subchild.tag == 'LifeArmorName':
                curr_unit["armor"] = subchild.attrib['value'][19:]
            elif subchild.tag == 'Food':
                curr_unit["supply"] = abs(float(subchild.attrib['value']))
            elif subchild.tag == 'WeaponArray':
                curr_unit["damage_type"], curr_unit["damage_base"], curr_unit['damage_rand'], curr_unit['attack_speed'] = get_weapon_type(subchild.attrib['Link'])
            elif subchild.tag == "CostResource" and subchild.attrib['index'] == 'Minerals':
                curr_unit["cost"] = subchild.attrib['value']
            elif subchild.tag == "CardLayouts":
                for card in subchild:
                    if card.attrib['Type'] == "Passive":
                        spell = {
                            'name': squad_data['Buttons'][card.attrib['Face']],
                            'description': rewrite_string(squad_data['Tooltips'][card.attrib['Face']])
                        }
                        curr_unit["abilities"].append(spell)
                    elif card.attrib['Type'] == "AbilCmd" and card.attrib['AbilCmd'][0:5] == "Train":
                        curr_unit['builder'] = card.attrib['AbilCmd'][5:].split(",", 1)[0]
                    elif card.attrib['Type'] == 'AbilCmd' and card.attrib['AbilCmd'][0:5] == "Sylph":
                        curr_unit['builder'] = "Sylphy"

        # print("UNIT: ", curr_unit)
        units[curr_unit['name'].lower()] = curr_unit

    # print(units)
    return units


def unit_total_costs(units):

    updated_units = units
    unit_tree = ET.parse('data/UnitData.xml')
    unit_root = unit_tree.getroot()

    for child in unit_root:
        if child.attrib.get('parent') != 'SquadronUnitTemplate':
            continue

        for subchild in child:
            if subchild.tag == "CardLayouts":
                for card in subchild:
                    if card.attrib['Type'] == "AbilCmd" and card.attrib['AbilCmd'][0:5] == 'Train':
                        upgrade_id = card.attrib['Face']
                        for unit in updated_units:
                            if updated_units[unit]['id'] == upgrade_id:
                                # print(updated_units[unit]['id'], child.attrib['id'])
                                updated_units[unit]['builder'] = card.attrib['AbilCmd'][5:].split(",", 1)[0]
                                updated_units[unit]['parent_id'] = child.attrib.get('id')

    for unit in updated_units:
        if not 'parent_id' in updated_units[unit]:
            continue

        for parent in updated_units:
            if updated_units[parent]['id'] == updated_units[unit]['parent_id']:
                if 'cost' in updated_units[parent]:
                    updated_units[unit]['parent_cost'] = updated_units[parent]['cost']
                if 'supply' in updated_units[parent]:
                    updated_units[unit]['parent_supply'] = updated_units[parent]['supply']
                if 'name' in updated_units[parent]:
                    updated_units[unit]['parent_name'] = updated_units[parent]['name']

    for unit in updated_units:
        if 'id' in updated_units[unit]:
            del updated_units[unit]['id']
        if 'parent_id' in updated_units[unit]:
            del updated_units[unit]['parent_id']

    return updated_units


def unit_data():
    button_data = get_data_strings("Button/Name/", 12)
    tooltip_data = get_data_strings("Button/Tooltip/", 15)
    unit_names = get_data_strings("Unit/Name/", 10)
    # weapon_names = get_data_strings("Weapon/Name/", 12)

    squad_data = {
        "Names": unit_names,
        "Tooltips": tooltip_data,
        "Buttons": button_data,
        # "WeaponNames": weapon_names
    }

    units_data = get_unit_data(squad_data)
    return unit_total_costs(units_data)
    # return units_data


if __name__ == "__main__":
    with open("units.json", 'w+') as f:
        f.write(json.dumps(unit_data()))