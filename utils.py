import xml.etree.ElementTree as ET
import re


def get_data_strings(prefix, prefix_length):
    data = {}
    with open('data/GameStrings.txt', 'r') as f:
        for line in f:
            if line[0:prefix_length] == prefix:
                sub_line = line[prefix_length:].split("=", 1)
                data[sub_line[0]] = sub_line[1].strip()
    return data


def get_weapon_damage(name):
    weapon_dmg_min = 0
    weapon_dmg_max = 0

    effect_tree = ET.parse('data/EffectData.xml')
    root = effect_tree.getroot()

    for child in root:
        if child.attrib['id'] == name:
            dmg_amount = ""
            dmg_rand = ""
            for subchild in child:
                if subchild.tag == 'Amount':
                    dmg_amount = subchild.attrib['value']
                elif subchild.tag == 'Random':
                    dmg_rand = subchild.attrib['value']

            weapon_dmg_max = dmg_amount
            weapon_dmg_min = dmg_rand

    return weapon_dmg_max, weapon_dmg_min


def get_weapon_type(name):
    dmg_type = ''
    dmg_min = 0
    dmg_max = 0
    attack_speed = ""
    weapon_tree = ET.parse('data/WeaponData.xml')
    root = weapon_tree.getroot()

    for child in root:
        if child.attrib['id'] == name:
            dmg_parent = child.attrib['parent']
            if dmg_parent == 'NormalAttack':
                dmg_type = "Normal"
            elif dmg_parent == 'ChaosAttack':
                dmg_type = 'Chaos'
            elif dmg_parent == 'PiercingAttack':
                dmg_type = 'Piercing'
            elif dmg_parent == 'MagicAttack':
                dmg_type = 'Magic'
            elif dmg_parent == 'SiegeAttack':
                dmg_type = "Siege"
            for subchild in child:
                if subchild.tag == "DisplayEffect":
                    dmg_max, dmg_min = get_weapon_damage(subchild.attrib['value'])
                elif subchild.tag == "Period":
                    attack_speed = subchild.attrib['value']

    return dmg_type, dmg_max, dmg_min, attack_speed


def leading_strip(string):
    if string[0] == '0':
        return string[1:]
    else:
        return string


def rewrite_string(str):
    s = re.sub(r'<(s|c)[^>]*>', '**', str)
    s = re.sub(r'</(s|c)>', '**', s)
    s = re.sub(r'<n/>', '\n', s)
    s = re.sub(r'<n>', '', s)
    return s

def leading_strip(string):
    if string[0] == '0':
        return string[1:]
    else:
        return string


def rewrite_send(str):
    s = re.sub(r'<(s|c)[^>]*>', '', str)
    s = re.sub(r'</(s|c)>', '', s)
    s = re.sub(r'<n/>', '\n', s)
    s = re.sub(r'<n>', '', s)
    return s