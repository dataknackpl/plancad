from typing import Tuple, List, Dict, Callable
import itertools
from collections import deque

Activity = str
RoomSlot = Tuple[str, str]
Schedule = Dict[Activity, RoomSlot]
Constraint = Callable[[Schedule], bool]


class SchedulerError(Exception):
    pass


def zip_activites_slots(activities, slots):
    return {a: s for a, s in zip(activities, slots)}


def dummy_scheduler(
    activities: List[Activity], slots: List[RoomSlot], constraints: List[Constraint]
) -> Schedule:
    """ The most naive scheduler that totally ignores constraints
      and zips activities with slots. Rather PoC only """
    return zip_activites_slots(activities, slots)


def all_combination_scheduler(
    activities: List[Activity], slots: List[RoomSlot], constraints: List[Constraint]
) -> Schedule:
    """ Simple scheduler that scans through all combinations
        and tries return first that satisfy all constraints

        Very nice in concept  but extremally inefficient!
    """
    for slot_combination in itertools.combinations(slots, len(activities)):
        schedule = zip_activites_slots(activities, slot_combination)
        if all(c(schedule) for c in constraints):
            return schedule
    return {}


def naive_search_scheduler(
    activities: List[Activity], slots: List[RoomSlot], constraints: List[Constraint]
) -> Schedule:
    """ Scheduler which uses Deep First Search aproach """

    def get_next_unasigned_variable(schedule):
        for activity in activities:
            if activity not in schedule:
                return activity
        return None

    def get_possible_values(schedule, next_variable):
        used_values = set(schedule.values())
        return [v for v in slots if v not in used_values]

    queue: deque = deque()
    queue.append(dict())
    visited = set()

    while queue:
        schedule = queue.popleft()
        if frozenset(schedule.items()) in visited:
            continue

        if not all(c(schedule) for c in constraints):
            visited.add(frozenset(schedule.items()))
            continue

        next_variable = get_next_unasigned_variable(schedule)
        if not next_variable:
            return schedule  # We have a winner!

        possible_values = get_possible_values(schedule, next_variable)
        if possible_values:
            for value in reversed(possible_values):
                queue.appendleft({**schedule, next_variable: value})

        visited.add(frozenset(schedule.items()))

    return {}  # No solution found


def find_schedule(
    activities: List[Activity],
    slots: List[RoomSlot],
    constraints: List[Constraint] = [],
) -> Schedule:
    """ Finds a schedule that meets all constraints
        Returns map between Activity and RoomSlots, or empty dict if not possible
    """
    if len(activities) > len(slots):
        raise SchedulerError("Number of activities exceeds slots")

    # schedule = all_combination_scheduler(activities, slots, constraints)
    schedule = naive_search_scheduler(activities, slots, constraints)
    return schedule
