from typing import Tuple, List, Dict, Callable

Activity = str
RoomSlot = Tuple[str, str]


def find_schedule(
    activities: List[Activity], slots: List[RoomSlot], constraints: List[Callable] = []
) -> Dict[Activity, RoomSlot]:
    """ Finds a schedule that meets all constraints
        Returns map between Activity and RoomSlots, or empty dict if not possible
    """
    pass
