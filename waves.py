import xml.etree.ElementTree as ET
import json

from utils import get_data_strings, get_weapon_type, leading_strip


def get_wave_data(squad_data):
    waves = {}

    unit_tree = ET.parse('data/UnitData.xml')
    root = unit_tree.getroot()

    waves_tree = ET.parse('data/UserData.xml')
    wave_root = waves_tree.getroot()

    for child in root:
        if not (child.attrib.get('parent') == 'WaveCreepBase' and child.attrib.get('id')[0:4] == 'Wave'):
            continue

        current_wave = {
            "name": squad_data["Names"][child.attrib['id']],
            "wave": leading_strip(child.attrib['id'][4:]),
            "id": child.attrib['id'],
            "speed": "2.5",
            "radius": "0.375"
        }

        for subchild in child:
            if subchild.tag == "Speed":
                current_wave["speed"] = subchild.attrib['value']
            elif subchild.tag == 'KillResource' and subchild.attrib["index"] == "Minerals":
                current_wave['bounty'] = subchild.attrib['value']
            elif subchild.tag == 'Radius':
                current_wave['radius'] = subchild.attrib['value']
            elif subchild.tag == 'LifeMax':
                current_wave['life'] = subchild.attrib['value']
            elif subchild.tag == "LifeArmorName":
                current_wave["armor"] = subchild.attrib['value'][19:]
            elif subchild.tag == "WeaponArray":
                current_wave['damage_type'], current_wave['damage_base'], current_wave['damage_rand'], current_wave['attack_speed'] = get_weapon_type(subchild.attrib['Link'])

        for ud_inst in wave_root:
            if ud_inst.attrib['id'] != "SquadWaveClassic":
                continue

            for subchild in ud_inst:
                is_wave = False
                for wave_child in subchild:
                    if wave_child.tag == "GameLink" and wave_child.attrib['GameLink'] == current_wave['id']:
                        is_wave = True
                    if wave_child.tag == "Int" and is_wave is True:
                        current_wave['count'] = wave_child.attrib['Int']

        waves[current_wave['name'].lower()] = current_wave

    return waves


def wave_data():
    button_data = get_data_strings("Button/Name/", 12)
    tooltip_data = get_data_strings("Button/Tooltip/", 15)
    unit_names = get_data_strings("Unit/Name/", 10)

    squad_data = {
        "Names": unit_names,
        "Tooltips": tooltip_data,
        "Buttons": button_data,
    }

    return get_wave_data(squad_data)


if __name__ == "__main__":
    with open("waves.json", 'w+') as f:
        f.write(json.dumps(wave_data()))