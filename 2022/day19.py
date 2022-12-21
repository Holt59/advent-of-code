# -*- encoding: utf-8 -*-

import sys
from typing import Literal

import numpy as np
import parse
from tqdm import tqdm

Reagent = Literal["ore", "clay", "obsidian", "geode"]
REAGENTS: tuple[Reagent, ...] = (
    "ore",
    "clay",
    "obsidian",
    "geode",
)

IntOfReagent = dict[Reagent, int]


class State:
    robots: IntOfReagent
    reagents: IntOfReagent

    def __init__(
        self,
        robots: IntOfReagent | None = None,
        reagents: IntOfReagent | None = None,
    ):
        if robots is None:
            assert reagents is None
            self.reagents = {reagent: 0 for reagent in REAGENTS}
            self.robots = {reagent: 0 for reagent in REAGENTS}
            self.robots["ore"] = 1
        else:
            assert robots is not None and reagents is not None
            self.robots = robots
            self.reagents = reagents

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, State)
            and self.robots == other.robots
            and self.reagents == other.reagents
        )

    def __hash__(self) -> int:
        return hash(tuple((self.robots[r], self.reagents[r]) for r in REAGENTS))

    def __str__(self) -> str:
        return "State({}, {})".format(
            "/".join(str(self.robots[k]) for k in REAGENTS),
            "/".join(str(self.reagents[k]) for k in REAGENTS),
        )

    def __repr__(self) -> str:
        return str(self)


def dominates(lhs: State, rhs: State):
    return all(
        lhs.robots[r] >= rhs.robots[r] and lhs.reagents[r] >= rhs.reagents[r]
        for r in REAGENTS
    )


lines = sys.stdin.read().splitlines()

blueprints: list[dict[Reagent, IntOfReagent]] = []
for line in lines:
    r = parse.parse(
        "Blueprint {}: "
        "Each ore robot costs {:d} ore. "
        "Each clay robot costs {:d} ore. "
        "Each obsidian robot costs {:d} ore and {:d} clay. "
        "Each geode robot costs {:d} ore and {:d} obsidian.",
        line,
    )

    blueprints.append(
        {
            "ore": {"ore": r[1]},
            "clay": {"ore": r[2]},
            "obsidian": {"ore": r[3], "clay": r[4]},
            "geode": {"ore": r[5], "obsidian": r[6]},
        }
    )


def run(blueprint: dict[Reagent, dict[Reagent, int]], max_time: int) -> int:

    # since we can only build one robot per time, we do not need more than X robots
    # of type K where X is the maximum number of K required among all robots, e.g.,
    # in the first toy blueprint, we need at most 4 ore robots, 14 clay ones and 7
    # obsidian ones
    maximums = {
        name: max(blueprint[r].get(name, 0) for r in REAGENTS) for name in REAGENTS
    }

    state_after_t: dict[int, set[State]] = {0: [State()]}

    for t in range(1, max_time + 1):

        # list of new states at the end of step t that we are going to prune later
        states_for_t: set[State] = set()

        for state in state_after_t[t - 1]:
            robots_that_can_be_built = [
                robot
                for robot in REAGENTS
                if all(
                    state.reagents[reagent] >= blueprint[robot].get(reagent, 0)
                    for reagent in REAGENTS
                )
            ]

            states_for_t.add(
                State(
                    robots=state.robots,
                    reagents={
                        reagent: state.reagents[reagent] + state.robots[reagent]
                        for reagent in REAGENTS
                    },
                )
            )

            if "geode" in robots_that_can_be_built:
                robots_that_can_be_built = ["geode"]
            else:
                robots_that_can_be_built = [
                    robot
                    for robot in robots_that_can_be_built
                    if state.robots[robot] < maximums[robot]
                ]

            for robot in robots_that_can_be_built:
                robots = state.robots.copy()
                robots[robot] += 1
                reagents = {
                    reagent: state.reagents[reagent]
                    + state.robots[reagent]
                    - blueprint[robot].get(reagent, 0)
                    for reagent in REAGENTS
                }
                states_for_t.add(State(robots=robots, reagents=reagents))

        # use numpy to switch computation of dominated states -> store each state
        # as a 8 array and use numpy broadcasting to find dominated states
        states_after = np.asarray(list(states_for_t))
        np_states = np.array(
            [
                [state.robots[r] for r in REAGENTS]
                + [state.reagents[r] for r in REAGENTS]
                for state in states_after
            ]
        )

        to_keep = []
        while len(np_states) > 0:
            first_dom = (np_states[1:] >= np_states[0]).all(axis=1).any()

            if first_dom:
                np_states = np_states[1:]
            else:
                to_keep.append(np_states[0])
                np_states = np_states[1:][~(np_states[1:] <= np_states[0]).all(axis=1)]

        state_after_t[t] = {
            State(
                robots=dict(zip(REAGENTS, row[:4])),
                reagents=dict(zip(REAGENTS, row[4:])),
            )
            for row in to_keep
        }

    return max(state.reagents["geode"] for state in state_after_t[max_time])


answer_1 = sum(
    (i_blueprint + 1) * run(blueprint, 24)
    for i_blueprint, blueprint in enumerate(blueprints)
)
print(f"answer 1 is {answer_1}")

answer_2 = run(blueprints[0], 32) * run(blueprints[1], 32) * run(blueprints[2], 32)
print(f"answer 2 is {answer_2}")
