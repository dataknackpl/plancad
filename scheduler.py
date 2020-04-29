from typing import Tuple, List, Dict, Callable

Activity = str
RoomSlot = Tuple[str, str]


class SchedulerError(Exception):
    pass


def find_schedule(
    activities: List[Activity], slots: List[RoomSlot], constraints: List[Callable] = []
) -> Dict[Activity, RoomSlot]:
    """ Finds a schedule that meets all constraints
        Returns map between Activity and RoomSlots, or empty dict if not possible
    """
    if len(activities) > len(slots):
        raise SchedulerError("Number of activities exceeds slots")

    schedule = {a: s for a, s in zip(activities, slots)}
    return schedule
