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


    StandardTile:Class
    :Inheritance (StandardTile -> Tile)

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
    WorldLevels:Association (World -> Level) {
        # At least one level
        target_lower_cardinality = 1;
    }

    # Level contains Tiles
    LevelTiles:Association (Level -> Tile) {
        # At least one tile
        target_lower_cardinality = 1;
    }

    # Creatures stand on a Tile
    StandingTile:Association (Creature -> Tile) {
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

    AdjacentTile:Association (Tile -> Tile) {
        target_lower_cardinality = 0;
        target_upper_cardinality = 4;
        
            constraint = ```
                conform = True;
                # Neighboring tile cannot be itself
                if get_source(this) == get_target(this): conform = False;
                
                # # Neighbors must be linked both ways
                # other_assoc = get_outgoing(get_target(this), "AdjacentTile")
                # if not other_assoc:
                #     conform = False
                # elif len(other_assoc) != 1:
                #     conform = False
                # elif get_target(other_assoc[0]) != get_source(this):
                #     conform = False
                
                # Neighbors must be in the same level
                source_assoc = get_incoming(get_source(this), "LevelTiles")
                target_assoc = get_incoming(get_target(this), "LevelTiles")
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

    # Tiles have adjacent tiles in directions
    AdjacentTile_direction:AttributeLink (AdjacentTile -> String) {
        name = "direction";
        optional = False;
    }

    # StandardTile can have an item
    StandardTileItem:Association (StandardTile -> Item) {
        target_lower_cardinality = 0;
        target_upper_cardinality = 1;
    }

    # Doors must be connected from one level to another
    ConnectingDoor:Association (Door -> Door) {
        target_lower_cardinality = 1;
        target_upper_cardinality = 1;
        constraint = ```
            conform = True;

            # Connecting door must be in another level
            target_level_ass = get_incoming(get_target(this), "LevelTiles")[0]
            source_level_ass = get_incoming(get_source(this), "LevelTiles")[0]
            if get_source(target_level_ass) == get_source(source_level_ass): conform = False;
            conform
        ```;
    }

    DoorKey:Association (Door -> Key) {
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
    
    WorldState:Class
    :Inheritance (WorldState -> State)
    
    CreatureState:Class
    :Inheritance (CreatureState -> State)

    ### ATTRIBUTES
    
    # Level has attribute name
    Clock_time:AttributeLink (Clock -> Integer) {
        name = "time";
        optional = False;
    }
    
    WorldState_collectedPoints:AttributeLink (WorldState -> Integer) {
        name = "collectedPoints";
        optional = False;
    }
    
    CreatureState_moved:AttributeLink (CreatureState -> Boolean) {
        name = "moved";
        optional = False;
    }
    
    ### ASSOCIATES
    WorldState_ass:Association (World -> WorldState) {
        target_lower_cardinality = 1;
        target_upper_cardinality = 1;
    }
    
    CreatureState_ass:Association (Creature -> CreatureState) {
        target_lower_cardinality = 1;
        target_upper_cardinality = 1;
    }
    
    HeroInventory:Association (Hero -> Item)
    

"""

m_rpg_def = """
    world:World 

    level1:Level{
        name = "level1";
    }
    
    level2:Level{
        name = "level2";
    }
    
    myHero:Hero {
        lives = 10;
    }
    
    monster:Monster {
        lives = 5;
    }
    
    #Tiles
    tile1:StandardTile
    tile2:StandardTile
    tile3:StandardTile
    tile4:Trap
    door1:Door

    tile5:StandardTile
    tile6:Obstacle
    tile7:StandardTile
    door2:Door


    #Items
    obj1:Objective{
        points = 10;
    }
    
    obj2:Objective{
        points = 90;
    }

    key1:Key
        
    #Links
    :WorldLevels (world -> level1)
    :WorldLevels (world -> level2)
    
    :LevelTiles (level1 -> tile1)
    :LevelTiles (level1 -> tile2)
    :LevelTiles (level1 -> tile3)
    :LevelTiles (level1 -> tile4)
    :LevelTiles (level1 -> door1)

    :LevelTiles (level2 -> tile5)
    :LevelTiles (level2 -> tile6)
    :LevelTiles (level2 -> tile7)
    :LevelTiles (level2 -> door2)

    #Connecting tiles
    
    :AdjacentTile (tile1 -> tile2){
        direction = "East";
    }
    :AdjacentTile (tile2 -> tile1){
        direction = "West";
    }
    
    :AdjacentTile (tile2 -> tile3){
        direction = "East";
    }
    :AdjacentTile (tile3 -> tile2){
        direction = "West";
    }
    
    :AdjacentTile (tile2 -> tile4){
        direction = "South";
    }
    :AdjacentTile (tile4 -> tile2){
        direction = "North";
    }
    
    :AdjacentTile (tile3 -> door1){
        direction = "South";
    }
    :AdjacentTile (door1 -> tile3){
        direction = "North";
    }
    
    :AdjacentTile (tile4 -> door1){
        direction = "East";
    }
    :AdjacentTile (door1 -> tile4){
        direction = "West";
    }
    
    
    :AdjacentTile (door2 -> tile5){
        direction = "North";
    }
    :AdjacentTile (tile5 -> door2){
        direction = "South";
    }
    
    :AdjacentTile (tile5 -> tile6){
        direction = "East";
    }
    :AdjacentTile (tile6 -> tile5){
        direction = "West";
    }
    
    :AdjacentTile (tile5 -> tile7){
        direction = "North";
    }
    :AdjacentTile (tile7 -> tile5){
        direction = "South";
    }


    :ConnectingDoor (door1 -> door2)
    :ConnectingDoor (door2 -> door1)
    
    
    :StandardTileItem (tile3 -> key1)
    :StandardTileItem (tile1 -> obj1)
    :StandardTileItem (tile7 -> obj2)
    
    
    :DoorKey (door1 -> key1)
    :DoorKey (door2 -> key1)
    
    :StandingTile (myHero -> tile2)
    :StandingTile (monster -> tile5)
"""

# DONE: add a valid instance of the additional runtime-information
rt_m_rpg_def = m_rpg_def + """
    c:Clock{
        time = 0;
    }

    myWorldState:WorldState {
        collectedPoints = 0;
    }
    
    myHeroState:CreatureState {
        moved = False;
    }
    
    monsterState:CreatureState {
        moved = False;
    }
    
    #Links
    :WorldState_ass (world -> myWorldState)
    :CreatureState_ass (myHero -> myHeroState)
    :CreatureState_ass (monster -> monsterState)

"""



# from state.devstate import DevState
# from bootstrap.scd import bootstrap_scd
# from concrete_syntax.textual_od import parser
# from framework.conformance import Conformance, render_conformance_check_result
#
# state = DevState()
# print("Loading mmm")
# mmm = bootstrap_scd(state)
# print("OK")
#
# print()
# print("Parsing mm")
# mm = parser.parse_od(
#         state,
#         m_text=rt_mm_rpg_def,
#         mm=mmm,
#     )
# print("OK")
#
#
# ### COMFORMNIG MODEL HOPEFULLY ###
#
# print()
# print("Parsing comforming model")
# m = parser.parse_od(
#         state,
#         m_text=rt_m_rpg_def,
#         mm=mm,
#     )
# print("OK")
#
# print()
# print("Is our model valid instance of meta model?")
# conf = Conformance(state, m, mm)
# print(render_conformance_check_result(conf.check_nominal()))
