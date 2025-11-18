from concrete_syntax.textual_od.parser import parse_od
from transformation.matcher import match_od
from transformation.ramify import ramify
from transformation.rule import RuleMatcherRewriter, PriorityActionGenerator
from util.loader import load_rules
import os.path


def get_filename(name, kind):
    file_dir = os.path.dirname(__file__)
    return f"{file_dir}/rules/r_{name}_{kind}.od"


def get_rules(current_state, rt_mm):
    print("Loading rules")
    rt_mm_ramified = ramify(current_state, rt_mm)
    matcher_rewriter = RuleMatcherRewriter(current_state, rt_mm, rt_mm_ramified)

    # DONE: Load other rules grouped by priority, add to action generator in order of priority
    rules = []

    # Moving
    rules.append(load_rules(current_state, get_filename, rt_mm_ramified,
                         ['move_hero_standardTile', 'move_hero_door', 'move_hero_trap', 'use_door']))

    # Picking up items
    rules.append(load_rules(current_state, get_filename, rt_mm_ramified, ['pick_up_key', 'pick_up_objective']))

    # Advance time
    rules.append(load_rules(current_state, get_filename, rt_mm_ramified, ['advance_time']))
    return PriorityActionGenerator(matcher_rewriter, rules)


class TerminationCondition:
    def __init__(self, state, rt_mm):
        self.state = state
        self.rt_mm_ramified = ramify(state, rt_mm)

        # Dict in the format "cause": "pattern"
        patterns_cs = {
            # DONE: Put the patterns for your termination conditions here
            "Lives are zero or below": """
                lives:RAM_Hero {
                    condition = `get_slot_value(this, "lives") <= 0`;
                }
                """,
            "All objectives are collected": """
                objectives:RAM_Hero {
                    condition = ```
                        totalObjectives = 0
                        objectives = get_all_instances("Objective")
                        for obj in objectives:
                            totalObjectives += get_slot_value(obj[1], "points")
                    
                        worldState = get_all_instances("WorldState")[0][1]
                        collected = get_slot_value(worldState,"collectedPoints")

                        collected == totalObjectives
                    ```;
                }
                """
        }

        self.patterns = {cause: parse_od(state, pattern_cs, self.rt_mm_ramified)
                         for cause, pattern_cs in patterns_cs.items()}

    def __call__(self, od):
        for cause in self.patterns:
            for match in match_od(self.state, od.m, od.mm, self.patterns[cause], self.rt_mm_ramified):
                # stop after the first match (no need to look for more matches):
                return cause
