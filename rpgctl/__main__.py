import argparse
import json
from typing import Dict, Iterable, Union


def get_matching_slugs(search: str, all_slugs: Iterable[str]):
    return [slug for slug in all_slugs if slug.startswith(search)]


def print_spell(spell: Dict[str, Union[str, int]]):
    print(spell["name"])
    print(spell["desc"])
    print()
    for key in ["ritual", "casting_time", "duration", "range", "components"]:
        print(f'{key.replace("_", " ")}: {spell[key]}')
    if "material" in spell:
        print(f'materials: {spell["material"]}')
    if spell["concentration"] == "yes":
        print("concentration")


if __name__ == "__main__":
    with open("rpgctl/spells.json") as f:
        spells = json.load(f)

    slugs_to_spells = {}
    for spell in spells:
        slug = spell["name"].lower().replace(" ", "").replace("/", "").replace("'", "")
        slugs_to_spells[slug] = spell

    parser = argparse.ArgumentParser(description="Commandline RPG reference tool.")
    parser.add_argument("spell", type=str)
    args = parser.parse_args()
    search = args.spell

    slugs = get_matching_slugs(search.lower(), slugs_to_spells.keys())

    if len(slugs) == 0:
        print("No spell matched your search")
    if len(slugs) > 1:
        print(f'Multiple matches: {" ".join(slugs)}')
    else:
        print_spell(slugs_to_spells[slugs[0]])
