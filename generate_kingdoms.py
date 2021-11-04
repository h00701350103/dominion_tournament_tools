#!/usr/bin/python3
"""Half-manual generation of dominion kingdom cards given a master list of supply cards"""
import random
import pprint

def main():
    """Generate all the shit"""
    kingdoms = []
    cards = []
    with open('all_cards_properties.txt', encoding='utf8') as file:
        for line in file:
            properties = line.strip().split(',')
            cards.append({'name': properties[0],
                'properties': [p.strip() for p in properties[1:]]})



    while True:
        kingdom = generate_kingdom(cards)
        if not kingdom[0]:
            break
        print(kingdom)
        kingdoms.append(kingdom)

        with open('raw_kindoms.txt', 'a', encoding='utf8') as file:
            file.write(f'{kingdom}\n')


    print(f'Remaining cards:')
    print(", ".join([c['name'] for c in cards]))



    print('prop counts')
    limited_props = ('horse', 'wisp', 'imp', 'ghost', 'boon', 'hex', 'spoils')
    unlimited_props = ('potion', 'platinum', 'shelters', 'ruins', 'wish')
    for prop in limited_props + unlimited_props:
        print(f'{prop}: {len([x for x in kingdoms if prop in x[1]])}')


    print(len(kingdoms))
    ## Check if it's possible to group these in four sets of 8 with only 2 of
    res = assign_sets(kingdoms, limited_props)
    for k_set in res:
        print(len(k_set))
        pprint.pprint(k_set)
    print()
    print(len(kingdoms))
    with open('kingdoms.txt', 'w', encoding='utf8') as file:
        for k_set,i in zip(res,range(len(res))):
            file.write(f'###Set {i}###\n')
            for kingdom in k_set:
                file.write(f'{kingdom}\n')

        file.write(f'###remaining kingdoms###')
        for kingdom in kingdoms:
            file.write(f'{kingdom}\n')




def generate_kingdom(cards):
    """Generate a kingdom"""
    print("Generating kingdom")
    kingdom_cards = []
    ways = 0
    landscapes = 0
    supply_cards = 0
    max_cards = 10

    skipped_cards = []
    properties = []

    while supply_cards < max_cards:
        if not len(cards):
            skipped_cards += kingdom_cards
            kingdom_cards = []
            break
        card_i = random.randrange(0, len(cards))
        card = cards.pop(card_i)
        if ways and 'way' in card['properties']:
            skipped_cards.append(card)
            continue
        if landscapes == 2 and 'landscape' in card['properties']:
            skipped_cards.append(card)
            continue
        if 'landscape' in card['properties']:
            landscapes += 1
            if 'way' in card['properties']:
                ways += 1
        else:
            supply_cards += 1
        if card['name'] == 'Young Witch':
            max_cards += 1
        kingdom_cards.append(card)
    cards += skipped_cards


    names = sorted([k['name'] for k in kingdom_cards])
    properties = [props for k in kingdom_cards for props in k['properties']]
    special_count = properties.count('special')
    shelter_count = properties.count('shelters')
    platina_count = properties.count('platinum')
    properties = list(set(properties))
    # shelters
    if ('shelters' in properties
            and random.randrange(0, supply_cards) >= shelter_count):
        properties.remove('shelters')
    # platinum
    if ('platinum' in properties
            and random.randrange(0, supply_cards) >= platina_count):
        properties.remove('platinum')
    if special_count:
        properties.extend(['special']*special_count)
    for skip in 'way', 'landscape':
        if skip in properties:
            properties.remove(skip)
    properties.sort()
    return names, properties


def assign_sets(kingdoms, limited_props, set_size=8, count=4):
    sets = []
    for i in range(count):
        sets.append([])
    sets = assign_set(kingdoms, sets, limited_props, set_size)
    return sets

def assign_set(kingdoms, sets, limited_props, set_size):
    if not valid_sets(sets, limited_props, set_size):
        return False
    if full_sets(sets, set_size):
        return sets
    kingdom = kingdoms.pop()
    for i in range(len(sets)):
        sets[i].append(kingdom)
        res = assign_set(kingdoms, sets, limited_props, set_size)
        if res:
            return res
        sets[i].remove(kingdom)
    return False

def valid_sets(sets, limited_props, set_size):
    for k_set in sets:
        if len(k_set) > set_size:
            return False
        for prop in limited_props:
            if len([k for k in k_set if prop in k[1]]) > 2:
                return False
    return True

def full_sets(sets, set_size):
    for k_set in sets:
        if len(k_set) != set_size:
            return False
    return True

if __name__ == '__main__':
    main()
