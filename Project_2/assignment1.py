mm = """
    ## Classes ##

    Hero:Class {
        constraint = ```
            conform = True
            
            # Lives cannot be negative
            if get_value(get_slot(this, "lives")) >= 0: conform = False
            
            # Hero cannot stand on obstacle tile
            # if todo : conform = False
            
            conform
        ```;
    }

    # Hero has attribute lives
    Hero_lives:AttributeLink (Hero -> Integer) {
        name = "lives";
        optional = False;
    }
    

    
    # Tiles    
    Tile:Class {
        abstract = True;
    }
    
    Tiles:AttributeLink (Tile -> Tile) {
        name = "northTile";
        optional = True;
    }
        
    Tiles:AttributeLink (Tile -> Tile) {
        name = "southTile";
        optional = True;
    }
        
    Tiles:AttributeLink (Tile -> Tile) {
        name = "eastTile";
        optional = True;
    }
    
    Tiles:AttributeLink (Tile -> Tile) {
        name = "westTile";
        optional = True;
    }
    
    StandardTile:Class {
        
    }
    :Inheritance (StandardTile -> Tile)
    
    Trap:Class {
    }
    :Inheritance (Trap -> Tile)
    
    Door:Class {
    }
    :Inheritance (Door -> Tile)
    
    Obstacle:Class {
    }
    :Inheritance (Obstacle -> Tile)
    
    
    # Hero must stand on a Tile
    Hero_tile:AttributeLink (Hero -> Tile) {
        name = "standingTile";
        optional = False;
    }
"""

m_c = """
    tile1:StandardTile{
    
    }

    myHero:Hero {
        lives = 10;
        standingTile = tile1
    }
"""

m_ic = """
    tile1:Obstacle{
    
    }

    myHero:Hero {
        # lives = -5;
        lives = 10;
        standingTile = tile1
    }
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

