# -*- encoding: utf-8 -*-

import heapq
import math
import sys
import time
from collections import defaultdict
from typing import Literal, TypedDict

import numpy as np
from tqdm import tqdm

Reagent = Literal["ore", "clay", "obsidian", "geode"]
REAGENTS: tuple[Reagent] = (
    "ore",
    "clay",
    "obsidian",
    "geode",
)

IntOfReagent = dict[Reagent, int]

lines = sys.stdin.read().splitlines()

blueprints: list[dict[Reagent, IntOfReagent]] = [
    {
        "ore": {"ore": 4},
        "clay": {"ore": 2},
        "obsidian": {"ore": 3, "clay": 14},
        "geode": {"ore": 2, "obsidian": 7},
    },
    {
        "ore": {"ore": 2},
        "clay": {"ore": 3},
        "obsidian": {"ore": 3, "clay": 8},
        "geode": {"ore": 3, "obsidian": 12},
    },
]


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

    def __lt__(self, other) -> bool:
        return isinstance(other, State) and tuple(
            (self.robots[r], self.reagents[r]) for r in REAGENTS
        ) > tuple((other.robots[r], other.reagents[r]) for r in REAGENTS)

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


MAX_TIME = 24
blueprint = blueprints[1]

# parents: dict[State, tuple[State | None, int]] = {State(): (None, 0)}
# queue = [(0, State())]
# visited: set[State] = set()
# at_time: dict[int, list[State]] = defaultdict(lambda: [])

# while queue:
#     time, state = heapq.heappop(queue)
#     if state in visited:
#         continue

#     print(time, state)

#     visited.add(state)

#     at_time[time].append(state)

#     if time > MAX_TIME:
#         continue

#     if len(queue) % 200 == 0:
#         print(len(queue), len(visited), time)

#     can_build_any: bool = False
#     for reagent in REAGENTS:
#         needed = blueprint[reagent]

#         if any(state.robots[r] == 0 for r in needed):
#             continue

#         time_to_complete = max(
#             max(
#                 math.ceil((needed[r] - state.reagents[r]) / state.robots[r])
#                 for r in needed
#             ),
#             0,
#         )

#         # if time_to_complete != 0:
#         #     continue

#         if time + time_to_complete + 1 > MAX_TIME:
#             continue

#         wait = time_to_complete + 1

#         reagents = {
#             r: state.reagents[r] + wait * state.robots[r] - needed.get(r, 0)
#             for r in REAGENTS
#         }

#         robots = state.robots.copy()
#         robots[reagent] += 1

#         state_2 = State(reagents=reagents, robots=robots)

#         if state_2 in visited:
#             continue

#         if any(dominates(state_v, state_2) for state_v in at_time[time + wait]):
#             continue

#         # print(time + wait)
#         # if any(dominates(state_3, state_2) for state_3 in at_time[time + wait]):
#         # print("?")
#         # continue

#         if state_2 not in parents or parents[state_2][1] > time + wait:
#             parents[state_2] = (state, time + wait)
#             heapq.heappush(queue, (time + wait, state_2))
#             can_build_any = True
#             at_time[time + wait].append(state_2)

#     if not can_build_any:
#         state_2 = State(
#             reagents={
#                 r: state.reagents[r] + state.robots[r] * (MAX_TIME - time)
#                 for r in REAGENTS
#             },
#             robots=state.robots,
#         )

#         if state_2 in visited:
#             continue

#         if state_2 not in parents or parents[state_2][1] > time + wait:
#             parents[state_2] = (state, MAX_TIME)
#             heapq.heappush(queue, (MAX_TIME, state_2))

# print(len(visited))
# print(max(state.reagents["geode"] for state in visited))

# exit()

# while states:
#     state = states.pop()
#     processed.append(state)

#     if state.time > MAX_TIME:
#         continue

#     if len(states) % 100 == 0:
#         print(len(states), len(processed), min((s.time for s in states), default=1))

#     can_build_any: bool = False
#     for reagent in REAGENTS:
#         needed = blueprint[reagent]

#         if any(state.robots[r] == 0 for r in needed):
#             continue

#         time_to_complete = max(
#             max(
#                 math.ceil((needed[r] - state.reagents[r]) / state.robots[r])
#                 for r in needed
#             ),
#             0,
#         )

#         if state.time + time_to_complete + 1 > MAX_TIME:
#             continue

#         wait = time_to_complete + 1

#         reagents = {
#             r: state.reagents[r] + wait * state.robots[r] - needed.get(r, 0)
#             for r in REAGENTS
#         }

#         robots = state.robots.copy()
#         robots[reagent] += 1

#         can_build_any = True
#         state_2 = State(time=state.time + wait, reagents=reagents, robots=robots)
#         # print(f"{state} -> {state_2}")
#         states.add(state_2)

#         if not any(dominates(s2, state_2) for s2 in states):
#             states.add(state)

#         # print(f"can build {reagent} in {time_to_complete}")

#     if not can_build_any:
#         states.add(
#             State(
#                 time=MAX_TIME + 1,
#                 reagents={
#                     r: state.reagents[r] + state.robots[r] * (MAX_TIME - state.time)
#                     for r in REAGENTS
#                 },
#                 robots=state.robots,
#             )
#         )

#     if len(states) % 1000 == 0:
#         print("filtering")
#         states = {
#             s1
#             for s1 in states
#             if not any(dominates(s2, s1) for s2 in states if s2 is not s1)
#         }

#     # if len(states) > 4:
#     #     break

#     # break

# print(len(processed))
# print(max(state.reagents["geode"] for state in processed))

# exit()

# for t in range(1, 25):
#     states = set()
#     for state in state_after_t[t - 1]:
#         robots_that_can_be_built = [
#             robot
#             for robot in REAGENTS
#             if all(
#                 state.reagents[reagent] >= blueprint[robot].get(reagent, 0)
#                 for reagent in REAGENTS
#             )
#         ]

#         new_states = set()

#         # new reagents
#         reagents = {
#             reagent: state.reagents[reagent] + state.robots[reagent]
#             for reagent in REAGENTS
#         }

#         # if we can build anything, there is no point in waiting
#         if len(robots_that_can_be_built) != len(REAGENTS):
#             new_states.add(State(robots=state.robots, reagents=reagents))

#         for robot in robots_that_can_be_built:
#             robots = state.robots.copy()
#             robots[robot] += 1
#             reagents = {
#                 reagent: state.reagents[reagent]
#                 + state.robots[reagent]
#                 - blueprint[robot].get(reagent, 0)
#                 for reagent in REAGENTS
#             }
#             new_states.add(State(robots=robots, reagents=reagents))

#         new_states = [
#             s1
#             for s1 in new_states
#             if not any(s1 is not s2 and dominates(s2, s1) for s2 in new_states)
#         ]

#         states = {
#             s1 for s1 in states if not any(dominates(s2, s1) for s2 in new_states)
#         }
#         states.update(new_states)

#     state_after_t[t] = states

# exit()


MAX_TIME = 24
blueprint = blueprints[0]

state_after_t: dict[int, list[State]] = {0: [State()]}

for t in range(1, 25):
    print(t, len(state_after_t[t - 1]))

    bests_for_robots: dict[tuple[int, ...], list[State]] = {}
    bests_for_reagents: dict[tuple[int, ...], list[State]] = {}

    state_after_t[t] = []

    t1 = time.time()

    for state in state_after_t[t - 1]:
        robots_that_can_be_built = [
            robot
            for robot in REAGENTS
            if all(
                state.reagents[reagent] >= blueprint[robot].get(reagent, 0)
                for reagent in REAGENTS
            )
        ]

        # print(t, robots_that_can_be_built)
        new_states: set[State] = set()

        # new reagents
        reagents = {
            reagent: state.reagents[reagent] + state.robots[reagent]
            for reagent in REAGENTS
        }

        # if we can build anything, there is no point in waiting
        new_states.add(State(robots=state.robots, reagents=reagents))

        for robot in robots_that_can_be_built:
            robots = state.robots.copy()
            robots[robot] += 1
            reagents = {
                reagent: state.reagents[reagent]
                + state.robots[reagent]
                - blueprint[robot].get(reagent, 0)
                for reagent in REAGENTS
            }
            new_states.add(State(robots=robots, reagents=reagents))

        for s1 in new_states:
            r1 = tuple(s1.robots[r] for r in REAGENTS)
            if r1 not in bests_for_robots:
                bests_for_robots[r1] = [s1]
            else:
                is_dominated = False
                for s2 in bests_for_robots[r1]:
                    if all(s2.reagents[r] >= s1.reagents[r] for r in REAGENTS):
                        is_dominated = True
                        break
                if not is_dominated:
                    bests_for_robots[r1].append(s1)

            r2 = tuple(s1.reagents[r] for r in REAGENTS)
            if r2 not in bests_for_reagents:
                bests_for_reagents[r2] = [s1]
            else:
                is_dominated = False
                for s2 in bests_for_reagents[r2]:
                    if all(s2.robots[r] >= s1.robots[r] for r in REAGENTS):
                        is_dominated = True
                        break
                if not is_dominated:
                    bests_for_reagents[r2].append(s1)
        # state_after_t[t].extend(new_states)

    t2 = time.time()

    for bests in bests_for_robots.values():
        dominated = [False for _ in range(len(bests))]
        for i_s1, s1 in enumerate(bests):
            if dominated[i_s1]:
                continue
            for i_s2, s2 in enumerate(bests[i_s1 + 1 :], start=i_s1 + 1):
                if dominated[i_s2]:
                    continue
                if all(s1.reagents[r] >= s2.reagents[r] for r in REAGENTS):
                    dominated[i_s2] = True
        state_after_t[t].extend(
            s1 for i_s1, s1 in enumerate(bests) if not dominated[i_s1]
        )
    for bests in bests_for_reagents.values():
        dominated = [False for _ in range(len(bests))]
        for i_s1, s1 in enumerate(bests):
            if dominated[i_s1]:
                continue
            for i_s2, s2 in enumerate(bests[i_s1 + 1 :], start=i_s1 + 1):
                if dominated[i_s2]:
                    continue
                if all(s1.robots[r] >= s2.robots[r] for r in REAGENTS):
                    dominated[i_s2] = True
        state_after_t[t].extend(
            s1 for i_s1, s1 in enumerate(bests) if not dominated[i_s1]
        )

    t3 = time.time()

    np_states = np.array(
        [
            [state.robots[r] for r in REAGENTS] + [state.reagents[r] for r in REAGENTS]
            for state in state_after_t[t]
        ]
    )
    dominated = np.zeros(len(np_states), dtype=bool)

    t4 = time.time()

    # c = (np_states[None, :, :] <= np_states[:, None, :]).all(axis=-1)
    # c[np.arange(len(np_states)), np.arange(len(np_states))] = False
    # dominated = c.any(axis=0)

    for i in range(len(np_states)):
        if dominated[i]:
            continue
        dominated[i] = not (np_states[i + 1 :] <= np_states[i]).any(axis=1)

        dominated[i + 1 :] = (np_states[i + 1 :] <= np_states[i]).all(axis=1)

    t5 = time.time()

    state_after_t[t] = list(np.array(state_after_t[t])[~dominated])

    t6 = time.time()

    print(
        "->",
        t,
        len(state_after_t[t]),
        dominated.sum(),
        t2 - t1,
        t3 - t2,
        t4 - t3,
        t5 - t4,
        t6 - t5,
    )

    # print("->", len(state_after_t[t]))

    # dominated = [False for _ in range(len(state_after_t[t]))]
    # keep = set()
    # for i_s1, s1 in enumerate(tqdm(state_after_t[t])):
    #     if dominated[i_s1]:
    #         continue
    #     for i_s2, s2 in enumerate(state_after_t[t][i_s1 + 1 :], start=i_s1 + 1):
    #         if dominated[i_s2]:
    #             continue

    #         if dominates(s1, s2):
    #             dominated[i_s2] = True
    #         elif dominates(s2, s1):
    #             dominated[i_s1] = True
    #             break

    #     if not dominated[i_s1]:
    #         keep.add(s1)

    # state_after_t[t] = list(keep)

    # print(len(state_after_t[t]))
    # print(sum(dominated))
    # break

print(max(state.reagents["geode"] for state in state_after_t[24]))
