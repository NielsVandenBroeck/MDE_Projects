import random
from functools import partial
from api.od import ODAPI
from transformation.cloner import clone_od


def precondition_creature_alive(od: ODAPI, creature: str):
    # Example for a pre-condition
    return od.get_slot_value(od.get(creature), "lives") > 0


def precondition_can_use_door(od: ODAPI, door: str):
    # DONE: Check whether the door can be used by the Hero: Do they have the matching Key?
    # Get required key of door
    key = od.get_target(od.get_outgoing(od.get(door), "DoorKey")[0])

    # Check if key in inventory of hero
    hero = od.get_all_instances("Hero")[0][1]
    for item_assoc in od.get_outgoing(hero, "HeroInventory"):
        if od.get_target(item_assoc) == key:
            return True
    return False

def precondition_creature_can_move(od: ODAPI, target_tile: str):
    # DONE: Check whether the target_tile can be occupied by a creature, i.e. it's not an Obstacle
    return od.get_type_name(od.get(target_tile)) != "Obstacle"

def precondition_fight_possible(od: ODAPI):
    # TODO: Check whether two creatures are on the same Tile so fighting is possible in the current state
    raise NotImplementedError


def mark_as_moved(od: ODAPI, creature_name: str):
    # DONE: Implement the Helper function to mark the creature as moved
    creatureState = od.get_target(od.get_outgoing(od.get(creature_name), "CreatureState_ass")[0])
    od.set_slot_value(creatureState, "moved", True)

def action_use_door(od: ODAPI, door: str):
    # DONE: Move the Hero to the connected Door
    # Remove hero from door
    original_tile = od.get(door)
    assoc = od.get_incoming(original_tile, "StandingTile")[0]
    hero = od.get_source(assoc)
    od.delete(assoc)

    # Add hero to connected door
    target_tile = od.get_target(od.get_outgoing(original_tile, "ConnectingDoor")[0])
    od.create_link(link_name="test",assoc_name="StandingTile", src=hero, tgt=target_tile)

    mark_as_moved(od,od.get_name(hero))
    return [f"Hero used {door} and went to level ..."]

def action_move_monster(od: ODAPI, monster: str, target_tile: str):
    # TODO: Move the monster to the target_tile
    raise NotImplementedError


def action_move_hero(od: ODAPI, original_tile_name: str, target_tile_name: str):
    # DONE: Handle a move of the Hero, incl. all side effects when stepping on special Tiles
    descriptions = []

    # Remove hero from original tile
    original_tile = od.get(original_tile_name)
    assoc = od.get_incoming(original_tile, "StandingTile")[0]
    hero = od.get_source(assoc)
    od.delete(assoc)

    # Add hero to new tile
    target_tile = od.get(target_tile_name)
    od.create_link(link_name="test",assoc_name="StandingTile", src=hero, tgt=target_tile)
    descriptions.append(f"Hero moved to tile: {target_tile_name}.")

    mark_as_moved(od,od.get_name(hero))

    # Check new tile for effects
    # Trap
    if od.get_type_name(target_tile) == "Trap":
        lives = od.get_slot_value(hero, "lives")
        od.set_slot_value(hero, "lives", lives-1)
        descriptions.append(f"Hero moved into a trap and lost a life. Lives left: {lives-1}.")

    # Item
    if od.get_type_name(target_tile) == "StandardTile":
        items_assocs = od.get_outgoing(target_tile, "StandardTileItem")
        for item_assoc in items_assocs:
            item = od.get_target(item_assoc)
            od.create_link(link_name=f"item_{od.get_name(item)}", assoc_name="HeroInventory", src=hero, tgt=item)
            if od.get_type_name(item) == "Key":
                descriptions.append(f"Hero Found a key. Try opening some doors to check which one it belongs to.")
            elif od.get_type_name(item) == "Objective":
                points = od.get_slot_value(item, "points")
                # Add points to worldstate
                worldstate = od.get_all_instances("WorldState")[0][1]
                od.set_slot_value(worldstate, "collectedPoints", od.get_slot_value(worldstate,"collectedPoints")+ points)
                descriptions.append(f"Hero picked up an objective of {points} points")


    # Monster (fight function)
    # TODO FIGHT

    return descriptions


def action_fight(od: ODAPI, hero_name: str, monster_name: str):
    # TODO: Determine the winner of the fight and adjust lives accordingly
    raise NotImplementedError


def action_advance_time(od: ODAPI):
    # Example for an action: This advances the time and resets all creatures
    _, clock = od.get_all_instances("Clock")[0]
    time = od.get_slot_value(clock, "time")
    new_time = time + 1
    od.set_slot_value(clock, "time", new_time)
    for _, creature_state in od.get_all_instances("CreatureState"):
        od.set_slot_value(creature_state, "moved", False)

    return [f"Time updated to {new_time}"]


def get_actions(od: ODAPI):
    """
        Retrieve the actions that are possible in the current state
    """
    # Dictionary mapping "Action text" to the (partial) function that is executed
    actions = {}

    # DONE: Determine the currently possible actions and add them to the actions dictionary
    # Get the Hero's current tile
    heroTile = None
    allCreaturePositions = od.get_all_instances("StandingTile")
    for pos in allCreaturePositions:
        assert len(pos) == 2, "Invalid amount of StandingTiles"
        if od.get_type_name(od.get_source(pos[1])) == "Hero":
            heroTile = od.get_target(pos[1])
    assert heroTile, "Hero not found"

    heroTile_name = od.get_name(heroTile)
    # Get the surrounding tiles
    tiles = {}
    for dir in ["North", "East", "South", "West"]:
        tiles[dir] = od.get_outgoing(heroTile, f"Tile{dir}")
        if tiles[dir]:
            tiles[dir] = od.get_target(tiles[dir][0])
        else:
            tiles[dir] = None
    for k, v in tiles.items():
        if not v:
            continue
        tile_name = od.get_name(v)
        if precondition_creature_can_move(od, tile_name):
            actions[f"Move to the {k}"] = partial(action_move_hero, original_tile_name=heroTile_name, target_tile_name=tile_name)

    # Check if hero is located on door tile, make action in this case
    if od.get_type_name(heroTile) == "Door":
        if precondition_can_use_door(od, heroTile_name):
            actions["Use Door"] = partial(action_use_door, door=heroTile_name)

    # Check if at least one monster is present in this level. if so, add action to listen to monster
    heroLevel = od.get_incoming(heroTile,"LevelTiles")[0]
    for pos in allCreaturePositions:
        if od.get_type_name(od.get_source(pos[1])) == "Monster":
            monsterTile = od.get_target(pos[1])
            monsterLevel = od.get_incoming(monsterTile, "LevelTiles")[0]
            if monsterLevel == heroLevel:
                actions["Listen to Monsters"] = action_advance_time

    # If no other action is possible, add the (one and only) choice to advance time
    if len(actions) == 0:
        actions["Continue..."] = action_advance_time

    return make_actions_pure(actions.items(), od)


def make_actions_pure(actions, od):
    """
        Adjust the actions so they are executed on a cloned OD
    """
    # Copy model before modifying it
    def exec_pure(action_to_exec, original_od):
        cloned_rt_m = clone_od(original_od.state, original_od.m, original_od.mm)
        new_od = ODAPI(original_od.state, cloned_rt_m, original_od.mm)
        msgs = action_to_exec(new_od)
        return new_od, msgs

    for descr, action in actions:
        yield descr, partial(exec_pure, action, od)


def termination_condition(od: ODAPI):
    # DONE: implement the termination conditions, returning None means no termination condition is satisfied
    # Otherwise, return a string with the reason for termination

    # Check if hero has lives left
    hero = od.get_all_instances("Hero")[0][1]
    if not precondition_creature_alive(od, od.get_name(hero)):
        return "Hero died"

    # Check if all collectables are found
    objectives = od.get_all_instances("Objective")
    points = 0
    for obj in objectives:
        points += od.get_slot_value(obj[1], "points")

    worldState = od.get_all_instances("WorldState")[0][1]
    collected = od.get_slot_value(worldState,"collectedPoints")
    if collected == points:
        return "Game complete! All collectables are found"

    return None
