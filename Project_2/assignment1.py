mm = """
    ## Classes ##

    World:Class{
        # Exactly one world 
        lower_cardinality = 1;
        upper_cardinality = 1;
    }
    
    Level:Class{
        constraint = ```
            conform = True
            
            # Name cannot be empty
            if len(get_value(get_slot(this, "name"))) == 0: conform = False
            conform
        ```;
    }
    
    
    Hero:Class {
        # Exactly one hero
        lower_cardinality = 1;
        upper_cardinality = 1;
        
        constraint = ```
            conform = True
            
            # Lives cannot be negative
            if get_value(get_slot(this, "lives")) < 0: conform = False
            
            conform
        ```;
    }

    
    # Tiles    
    Tile:Class {
        abstract = True;
    }
    
    
    Standard_tile:Class {
        #todo item
    }
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
    
    Objective:Class
    :Inheritance (Objective -> Item)
    
    
    ## ATTRIBUTES ##
    
    # Level has attribute name
    Level_name:AttributeLink (Level -> String) {
        name = "name";
        optional = False;
    }
    
    # Hero has attribute lives
    Hero_lives:AttributeLink (Hero -> Integer) {
        name = "lives";
        optional = False;
    }
    
    # Objective has points
    Objective_points:AttributeLink (Objective -> Integer) {
        name = "points";
        optional = False;
        
        constraint = ```
            conform = True;
            objectives = get_all_instances("Objective")
            sum = 0
            for objective in objectives:
                sum += get_value(get_slot(objective[1], "points"))
            if sum > 100: conform = False
            conform
        ```;
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

    
    # Hero stands on a Tile
    Standing_tile:Association (Hero -> Tile) {
        # Hero stands on exactly one tile
        target_lower_cardinality = 1;
        target_upper_cardinality = 1;
        constraint = ```
            conform = True;
            # Hero cannot stand on obstacle tile
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
            conform
        ```;
    }
    
    Connecting_door:Association (Door -> Door) {
        target_lower_cardinality = 1;
        target_upper_cardinality = 1;
        constraint = ```
            conform = True;

            # connecting door must be in another level
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

m_c = """
    world:World 

    level1:Level{
        name = "level1";
    }
    
    level2:Level{
        name = "level2";
    }

    tile1:Standard_tile
    tile2:Standard_tile
    tile3:Standard_tile
    tile4:Standard_tile

    obj1:Objective{
        points = 80;
    }
    obj2:Objective{
        points = 10;
    }

    door1:Door
    key1:Key
    door2:Door
    key2:Key
        
    :World_levels (world -> level1)
    :World_levels (world -> level2)
    
    :Level_tiles (level1 -> tile1)
    :Level_tiles (level1 -> tile2)
    :Level_tiles (level2 -> tile3)
    :Level_tiles (level2 -> tile4)
    
    :Level_tiles (level1 -> door1)
    :Level_tiles (level2 -> door2)
    
    :Connecting_door (door1 -> door2)
    :Connecting_door (door2 -> door1)
    
    :Door_key (door1 -> key1)
    :Door_key (door2 -> key2)


    myHero:Hero {
        lives = 10;
    }
    
    :Standing_tile (myHero -> tile1)
"""

m_ic = """
    world:World 
    level1:Level{
        name = "level1";
    }

    # Should give error -> hero cannot stand on obstacle tile
    tile:Obstacle

    myHero:Hero {
        # lives = -5;
        lives = 10;
    }
    
    :World_levels (world -> level1)
    :Level_tiles (level1 -> tile)
    :Standing_tile (myHero -> tile)
    
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
        m_text=mm,
        mm=mmm,
    )
print("OK")


### COMFORMNIG MODEL HOPEFULLY ###

print()
print("Parsing comforming model")
m = parser.parse_od(
        state,
        m_text=m_c,
        mm=mm,
    )
print("OK")

print()
print("Is our model valid instance of meta model?")
conf = Conformance(state, m, mm)
print(render_conformance_check_result(conf.check_nominal()))

### NON COMFORMING MODEL HOPEFULLY ###

print()
print("Parsing non-comforming model")
m = parser.parse_od(
        state,
        m_text=m_ic,
        mm=mm,
    )
print("OK")

print()
print("Is our model valid instance of meta model? (hopefully not)")
conf = Conformance(state, m, mm)
print(render_conformance_check_result(conf.check_nominal()))

