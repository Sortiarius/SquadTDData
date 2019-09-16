import xml.etree.ElementTree as ET
import json

from utils import get_data_strings, get_weapon_type, rewrite_send, get_weapon_damage


def get_send_data(squad_data):
    sends = {}

    unit_tree = ET.parse('data/UnitData.xml')
    root = unit_tree.getroot()

    for child in root:
        if not child.attrib.get("parent") == "SendBase":
            continue

        current_send = {
            "name": squad_data["Names"][child.attrib['id']],
            "speed": "2.5",
            "radius": "0.375",
            "id": child.attrib['id'],
            "details": rewrite_send(squad_data['Tooltips'][child.attrib['id']])
        }

        for subchild in child:
            if subchild.tag == "LifeMax":
                current_send['life'] = subchild.attrib['value']
            elif subchild.tag == "Speed":
                current_send['speed'] = subchild.attrib['value']
            elif subchild.tag == "Radius":
                current_send['radius'] = subchild.attrib['value']
            elif subchild.tag == "CostResource" and subchild.attrib['index'] == "Vespene":
                current_send['cost'] = subchild.attrib['value']
            elif subchild.tag == "KillResource" and subchild.attrib['index'] == "Minerals":
                current_send['bounty'] = subchild.attrib['value']
            elif subchild.tag == "LifeArmorName":
                current_send['armor'] = subchild.attrib['value'][19:]
            elif subchild.tag == "WeaponArray":
                current_send['damage_type'], current_send['damage_base'], current_send['damage_rand'], current_send['attack_speed'] = get_weapon_type(subchild.attrib['Link'])
                if current_send['damage_base'] == 0:
                    current_send['damage_base'], current_send['damage_rand'] = get_weapon_damage(subchild.attrib['Link'])

        sends[current_send['name'].lower()] = current_send

    return sends


def send_data():
    button_data = get_data_strings("Button/Name/", 12)
    tooltip_data = get_data_strings("Button/Tooltip/", 15)
    unit_names = get_data_strings("Unit/Name/", 10)

    squad_data = {
        "Names": unit_names,
        "Tooltips": tooltip_data,
        "Buttons": button_data,
    }

    return get_send_data(squad_data)


if __name__ == "__main__":
    with open("sends.json", 'w+') as f:
        f.write(json.dumps(send_data()))