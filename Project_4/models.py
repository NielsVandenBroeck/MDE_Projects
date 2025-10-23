mm_rpg_def = """
    ## Classes ##

    World:Class{
        # Exactly one world 
        lower_cardinality = 1;
        upper_cardinality = 1;
        
        constraint = ```
            conform = True;
            
            ### Objectives cannot sum to more than 100 total ###
            objectives = get_all_instances("Objective")
            sum = 0
            for objective in objectives:
                sum += get_value(get_slot(objective[1], "points"))
            if sum > 100: conform = False
            
            conform
        ```;
    }

    Level:Class{
        constraint = ```
            conform = True

            # Name cannot be empty
            if len(get_value(get_slot(this, "name"))) == 0: conform = False
            conform
        ```;
    }

    Creature:Class {
        abstract = True;
        
        constraint = ```
            conform = True

            # Lives cannot be negative
            if get_value(get_slot(this, "lives")) < 0: conform = False

            conform
        ```;
    }

    Hero:Class {
        # Exactly one hero
        lower_cardinality = 1;
        upper_cardinality = 1;
    }
    :Inheritance (Hero -> Creature)


    Monster:Class
    :Inheritance (Monster -> Creature)

    # Tiles    
    Tile:Class {
        abstract = True;
    }


    Standard_tile:Class
    :Inheritance (Standard_tile -> Tile)

    Trap:Class
    :Inheritance (Trap -> Tile)

    Door:Class
    :Inheritance (Door -> Tile)

    Obstacle:Class
    :Inheritance (Obstacle -> Tile)

    Item:Class

    Key:Class
    :Inheritance (Key -> Item)

    Objective:Class {
        constraint = ```
            conform = True
    
            # Points cannot be negative
            if get_value(get_slot(this, "points")) < 0: conform = False
    
            conform
        ```;
    }
    :Inheritance (Objective -> Item)


    ## ATTRIBUTES ##

    # Level has attribute name
    Level_name:AttributeLink (Level -> String) {
        name = "name";
        optional = False;
    }

    # Creatures have attribute lives
    Creature_lives:AttributeLink (Creature -> Integer) {
        name = "lives";
        optional = False;
    }

    # Objective has points
    Objective_points:AttributeLink (Objective -> Integer) {
        name = "points";
        optional = False;  
    }

    ## ASSOCIATIONS ##

    # World contains Levels 
    World_levels:Association (World -> Level) {
        # At least one level
        target_lower_cardinality = 1;
    }

    # Level contains Tiles
    Level_tiles:Association (Level -> Tile) {
        # At least one tile
        target_lower_cardinality = 1;
    }

    # Creatures stand on a Tile
    Standing_tile:Association (Creature -> Tile) {
        # a creature can stand on maximum 1 tile
        target_upper_cardinality = 1;

        constraint = ```
            conform = True;
            # Creatures cannot stand on obstacle tile
            target = get_target(this)
            if get_type_name(target) == "Obstacle": conform = False;
            
            conform
        ```;
    }

    Tile_north:Association (Tile -> Tile) {
        target_lower_cardinality = 0;
        target_upper_cardinality = 1;


        constraint = ```
            conform = True;
            # Neighboring tile cannot be itself
            if get_source(this) == get_target(this): conform = False;
            
            # Neighbors must be linked both ways
            other_assoc = get_outgoing(get_target(this), "Tile_south")
            if not other_assoc:
                conform = False
            elif len(other_assoc) != 1:
                conform = False
            elif get_target(other_assoc[0]) != get_source(this):
                conform = False        
            
            # Neighbors must be in the same level
            source_assoc = get_incoming(get_source(this), "Level_tiles")
            target_assoc = get_incoming(get_target(this), "Level_tiles")
            if not source_assoc or not target_assoc:
                # Tile must belong to a level
                conform = False
            elif len(source_assoc) != 1 or len(target_assoc) != 1:
                conform = False
            elif get_source(source_assoc[0]) != get_source(target_assoc[0]):
                conform = False
            conform
        ```;
    }

    Tile_south:Association (Tile -> Tile) {
        target_lower_cardinality = 0;
        target_upper_cardinality = 1;

        constraint = ```
            conform = True;
            # Neighboring tile cannot be itself
            if get_source(this) == get_target(this): conform = False;
            
            # Neighbors must be linked both ways
            other_assoc = get_outgoing(get_target(this), "Tile_north")
            if not other_assoc:
                conform = False
            elif len(other_assoc) != 1:
                conform = False
            elif get_target(other_assoc[0]) != get_source(this):
                conform = False        
            
            # Neighbors must be in the same level
            source_assoc = get_incoming(get_source(this), "Level_tiles")
            target_assoc = get_incoming(get_target(this), "Level_tiles")
            if not source_assoc or not target_assoc:
                # Tile must belong to a level
                conform = False
            elif len(source_assoc) != 1 or len(target_assoc) != 1:
                conform = False
            elif get_source(source_assoc[0]) != get_source(target_assoc[0]):
                conform = False
            conform
        ```;
    }

    Tile_east:Association (Tile -> Tile) {
        target_lower_cardinality = 0;
        target_upper_cardinality = 1;

        constraint = ```
            conform = True;
            # Neighboring tile cannot be itself
            if get_source(this) == get_target(this): conform = False;
            
            # Neighbors must be linked both ways
            other_assoc = get_outgoing(get_target(this), "Tile_west")
            if not other_assoc:
                conform = False
            elif len(other_assoc) != 1:
                conform = False
            elif get_target(other_assoc[0]) != get_source(this):
                conform = False        
                        
            # Neighbors must be in the same level
            source_assoc = get_incoming(get_source(this), "Level_tiles")
            target_assoc = get_incoming(get_target(this), "Level_tiles")
            if not source_assoc or not target_assoc:
                # Tile must belong to a level
                conform = False
            elif len(source_assoc) != 1 or len(target_assoc) != 1:
                conform = False
            elif get_source(source_assoc[0]) != get_source(target_assoc[0]):
                conform = False
            conform
        ```;
    }

    Tile_west:Association (Tile -> Tile) {
        target_lower_cardinality = 0;
        target_upper_cardinality = 1;

        constraint = ```
            conform = True;
            # Neighboring tile cannot be itself
            if get_source(this) == get_target(this): conform = False;
            
            # Neighbors must be linked both ways
            other_assoc = get_outgoing(get_target(this), "Tile_east")
            if not other_assoc:
                conform = False
            elif len(other_assoc) != 1:
                conform = False
            elif get_target(other_assoc[0]) != get_source(this):
                conform = False        
            
            # Neighbors must be in the same level
            source_assoc = get_incoming(get_source(this), "Level_tiles")
            target_assoc = get_incoming(get_target(this), "Level_tiles")
            if not source_assoc or not target_assoc:
                # Tile must belong to a level
                conform = False
            elif len(source_assoc) != 1 or len(target_assoc) != 1:
                conform = False
            elif get_source(source_assoc[0]) != get_source(target_assoc[0]):
                conform = False
            conform
        ```;
    }

    # StandardTile can have an item
    StandardTile_item:Association (Standard_tile -> Item) {
        target_lower_cardinality = 0;
        target_upper_cardinality = 1;
    }

    # Doors must be connected from one level to another
    Connecting_door:Association (Door -> Door) {
        target_lower_cardinality = 1;
        target_upper_cardinality = 1;
        constraint = ```
            conform = True;

            # Connecting door must be in another level
            target_level_ass = get_incoming(get_target(this), "Level_tiles")[0]
            source_level_ass = get_incoming(get_source(this), "Level_tiles")[0]
            if get_source(target_level_ass) == get_source(source_level_ass): conform = False;
            conform
        ```;
    }

    Door_key:Association (Door -> Key) {
        target_lower_cardinality = 1;
        target_upper_cardinality = 1;
    }
"""

rt_mm_rpg_def = mm_rpg_def + """
    Clock:Class {
        
    }
    
    State:Class {
        abstract = True;
    }
    
    World_state:Class
    :Inheritance (World_state -> State)
    
    Creature_state:Class
    :Inheritance (Creature_state -> State)

    ### ATTRIBUTES
    
    # Level has attribute name
    Clock_time:AttributeLink (Clock -> Integer) {
        name = "time";
        optional = False;
    }
    
    Collected_points:AttributeLink (World_state -> Integer) {
        name = "collected_points";
        optional = False;
    }
    
    Creature_moved:AttributeLink (Creature_state -> Boolean) {
        name = "moved";
        optional = False;
    }
    
    ### ASSOCIATES
    World_state_ass:Association (World -> World_state) {
        target_lower_cardinality = 1;
        target_upper_cardinality = 1;
    }
    
    Creature_state_ass:Association (Creature -> Creature_state) {
        target_lower_cardinality = 1;
        target_upper_cardinality = 1;
    }
    
    Hero_inventory:Association (Hero -> Item)
    

"""

m_rpg_def = """
    c:Clock{
        time = 0;
    }
    
    
    world:World 
    myWorldState:World_state {
        collected_points = 0;
    }

    level1:Level{
        name = "level1";
    }
    
    level2:Level{
        name = "level2";
    }
    
    myHero:Hero {
        lives = 10;
    }
    myHeroState:Creature_state {
        moved = False;
    }
    
    monster:Monster {
        lives = 20;
    }
    monsterState:Creature_state {
        moved = False;
    }

    #Tiles
    tile1:Standard_tile
    tile2:Standard_tile
    tile3:Trap
    tile4:Obstacle
    door1:Door
    door2:Door


    #Items
    obj:Objective{
        points = 80;
    }

    key1:Key
    key2:Key
        
    #Links
    :World_state_ass (world -> myWorldState)
    :Creature_state_ass (myHero -> myHeroState)
    :Creature_state_ass (monster -> monsterState)

    
    :World_levels (world -> level1)
    :World_levels (world -> level2)
    
    :Level_tiles (level1 -> tile1)
    :Level_tiles (level1 -> tile2)
    :Level_tiles (level1 -> door1)

    :Level_tiles (level2 -> tile3)
    :Level_tiles (level2 -> tile4)
    :Level_tiles (level2 -> door2)

    #Connecting tiles
    :Tile_south (tile1 -> tile2)
    :Tile_north (tile2 -> tile1)
    :Tile_west (tile1 -> door1)
    :Tile_east (door1 -> tile1)

    :Tile_south (tile3 -> tile4)
    :Tile_north (tile4 -> tile3)
    :Tile_west (tile3 -> door2)
    :Tile_east (door2 -> tile3)


    :Connecting_door (door1 -> door2)
    :Connecting_door (door2 -> door1)
    
    :StandardTile_item (tile2 -> key1)
    :StandardTile_item (tile1 -> obj)
    
    :Door_key (door1 -> key1)
    :Door_key (door2 -> key2)
    
    :Standing_tile (myHero -> tile1)
    :Standing_tile (monster -> tile1)
"""

# TODO: add a valid instance of the additional runtime-information
rt_m_rpg_def = m_rpg_def + """

"""



from state.devstate import DevState
from bootstrap.scd import bootstrap_scd
from concrete_syntax.textual_od import parser
from framework.conformance import Conformance, render_conformance_check_result

state = DevState()
print("Loading mmm")
mmm = bootstrap_scd(state)
print("OK")

print()
print("Parsing mm")
mm = parser.parse_od(
        state,
        m_text=rt_mm_rpg_def,
        mm=mmm,
    )
print("OK")


### COMFORMNIG MODEL HOPEFULLY ###

print()
print("Parsing comforming model")
m = parser.parse_od(
        state,
        m_text=m_rpg_def,
        mm=mm,
    )
print("OK")

print()
print("Is our model valid instance of meta model?")
conf = Conformance(state, m, mm)
print(render_conformance_check_result(conf.check_nominal()))
