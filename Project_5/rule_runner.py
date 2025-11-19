from api.od import ODAPI
from bootstrap.scd import bootstrap_scd
from state.devstate import DevState
from util.loader import parse_and_check, load_rules
from Project_5.models import mm_rpg_def, m_rpg_def, rt_mm_rpg_def, rt_m_rpg_def
from Project_5.simulator import RPGSimulator

from assignment5 import get_rules, TerminationCondition


def render_text(od: ODAPI):
    # Done: Implement, so a short description of the current state is printed
    txt = "CURRENT STATE\n"
    HeroText = ""
    MonstersTexts = "---MONSTERS---\n"
    monster_present = False

    creatures = od.get_all_instances("Creature")
    for creature in creatures:
        creature = creature[1]
        creatureState = od.get_target(od.get_outgoing(creature, "CreatureState_ass")[0])
        creatureMoved = od.get_slot_value(creatureState, "moved")
        creatureFought = od.get_slot_value(creatureState, "fought")
        if od.get_type_name(creature) == "Hero":
            HeroText = "---HERO---\n"

            # Name
            name = od.get_name(creature)
            HeroText += f"Name: {name}\n"

            # Lives
            lives = od.get_slot_value(creature, "lives")
            HeroText += f"Lives: {lives}\n"

            # Fought
            HeroText += f"Fought: {creatureFought}\n"

            # Level
            heroTile = od.get_target(od.get_outgoing(creature, "StandingTile")[0])
            heroLevel = od.get_source(od.get_incoming(heroTile, "LevelTiles")[0])
            HeroText += f"Located in level: {od.get_name(heroLevel)} at tile: {od.get_name(heroTile)}\n"

            # Moved
            HeroText += f"Moved: {creatureMoved}\n"

            # Inventory
            HeroText += "Inventory:\n"
            inventory_assocs = od.get_outgoing(creature, "HeroInventory")
            if not inventory_assocs:
                HeroText += "\t Empty \n"
            for item_assoc in inventory_assocs:
                item = od.get_target(item_assoc)
                HeroText += '\t' + od.get_name(item) + '\n'

            # Collected Points
            worldState = od.get_all_instances("WorldState")[0][1]
            collectedPoints = od.get_slot_value(worldState, "collectedPoints")
            HeroText += f"Collected points: {collectedPoints}\n"

            HeroText += "\n"


        else:
            monster_present = True

            # Name
            name = od.get_name(creature)
            MonstersTexts += f"Name: {name}\n"

            # Lives
            lives = od.get_slot_value(creature, "lives")
            MonstersTexts += f"Lives: {lives}\n"

            # Fought
            MonstersTexts += f"Fought: {creatureFought}\n"

            # Level
            Tile = od.get_target(od.get_outgoing(creature, "StandingTile")[0])
            Level = od.get_source(od.get_incoming(Tile, "LevelTiles")[0])
            MonstersTexts += f"Located in level: {od.get_name(Level)} at tile: {od.get_name(Tile)}\n"

            # Moved
            MonstersTexts += f"Moved: {creatureMoved}\n"

            MonstersTexts += "-------------\n"

    # Print lives
    lives = od.get_slot_value(od.get_all_instances("Hero")[0][1], "lives")
    txt += f"[{lives} lives] "

    txt = HeroText
    if monster_present:
        txt += MonstersTexts
    return txt


state = DevState()
scd_mm = bootstrap_scd(state)

# Static Models
rpg_mm = parse_and_check(state, mm_rpg_def, scd_mm, "MM for RPG")
rpg_m = parse_and_check(state, m_rpg_def, rpg_mm, "Model for RPG")
# Runtime Models
rt_rpg_mm = parse_and_check(state, rt_mm_rpg_def, scd_mm, "Runtime MM for RPG")
rt_rpg_m = parse_and_check(state, rt_m_rpg_def, rt_rpg_mm, "Runtime Model for RPG")

rule_generator = get_rules(state, rt_rpg_mm)
rule_sim = RPGSimulator(
    action_generator=rule_generator,
    termination_condition=TerminationCondition(state, rt_rpg_mm),
    renderer=render_text
)

rpg_od = ODAPI(state, rt_rpg_m, rt_rpg_mm)
rule_sim.run(rpg_od)
