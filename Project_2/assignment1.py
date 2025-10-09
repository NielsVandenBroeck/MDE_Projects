mm = """
    ## Classes ##

    Hero:Class {
        constraint = ```
            # Lives cannot be negative
            get_value(get_slot(this, "lives")) >= 0
        ```
    }

    # Hero has attribute lives
    Hero_lives:AttributeLink (Hero -> Integer) {
        name = "lives";
        optional = False;
    }
"""

m_c = """
    myHero:Hero {
        lives = 10;
    }
"""

m_ic = """
    myHero:Hero {
        lives = -5;
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

print()
print("Parsing model")
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
