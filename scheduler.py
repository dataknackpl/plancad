from typing import Tuple, List, Dict, Callable
import itertools

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

    schedule = all_combination_scheduler(activities, slots, constraints)
    return schedule
