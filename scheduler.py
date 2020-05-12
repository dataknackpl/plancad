from typing import List, Set, Dict, Tuple, Callable, Union
from collections import deque
from functools import reduce

Constraint = str


class RoomSlot:
    def __init__(self, value: str, attributes: Dict[str, str] = None):
        self.value = value
        self.attributes = attributes if attributes else {}

    def __repr__(self):
        return f"RoomSlot(value='{self.value}', attributes={self.attributes}"


class Activity:
    def __init__(self, name: str, constraints: List[Constraint] = None):
        self.name = name
        self.constraints = (
            [self._parse_constraint(c) for c in constraints] if constraints else []
        )

    @staticmethod
    def _parse_constraint(c: Constraint) -> Tuple[str, str, str]:
        """ Parse line string constraint into subject, operator, value tuple """
        subject, operator, value = c.split(" ")

        if operator != "==":
            raise ValueError(f"Not recognized operator '{operator}'")

        return (subject, operator, value)

    def is_slot_valid(self, slot: RoomSlot) -> bool:
        """ Slot is considered valid if matches all constrints """
        for c in self.constraints:
            subject = c[0]
            value = c[2]
            if subject not in slot.attributes:
                return False

            if slot.attributes[subject] != value:
                return False

        return True

    def __repr__(self):
        return self.name


Schedule = Dict[Activity, RoomSlot]


class SchedulerError(Exception):
    pass


def total_number_of_combinations(n: int, k: int) -> int:
    """ Calculate how many nodes at total needs to be visited """
    # num of combinations: n!/(n-k)!
    # assert n >= 1, f"n must be >= 1, was {n}"
    # assert k >= 1, f"k must be >= 1, was {k}"
    if n <= 0:
        return 0
    if k <= 0:
        return 0

    assert n >= k, f"{n=} cannot be smaller than {k=}"

    return reduce(lambda x, y: x * y, range(n, n - k, -1))


def generate_activity_slots_map(
    activities: List[Activity], slots: List[RoomSlot],
) -> Dict[Activity, List[RoomSlot]]:
    """ Utility function to get map of possible slots for activities """
    return {a: [s for s in slots if a.is_slot_valid(s)] for a in activities}


def search_scheduler(
    activities: List[Activity],
    slots: List[RoomSlot],
    progress_callback: Callable[[deque], None] = None,
) -> Schedule:
    """ Scheduler which uses Depth First Search approach """

    activity_slots_map = generate_activity_slots_map(activities, slots)

    def most_constrainted_variable(
        activities: List[Activity], used_values: Set[RoomSlot]
    ) -> Union[Activity, None]:
        if not activities:
            return None

        # Tuples of (available option count, activity)
        option_count = [
            (len(set(activity_slots_map[a]) - used_values), a) for a in activities
        ]
        options_count_sorted = sorted(option_count, key=lambda x: x[0])
        most_restricted_option = options_count_sorted[0]
        return most_restricted_option[1]  # The activity

    def get_next_unassigned_variable(schedule):
        unassigned_activities = [a for a in activities if a not in schedule]

        if not unassigned_activities:
            return None

        # find most constrained variable - mcv
        # which here is one with least possible values
        used_values = set(schedule.values())

        mcv = most_constrainted_variable(unassigned_activities, used_values)
        return mcv

    def get_possible_values(schedule, next_variable):
        used_values = set(schedule.values())
        return [v for v in activity_slots_map[next_variable] if v not in used_values]

    queue: deque = deque()
    queue.append(dict())

    while queue:
        if progress_callback:
            progress_callback(queue)
        schedule = queue.popleft()

        validation_checks = [
            a.is_slot_valid(s) for a, s in schedule.items() if a.constraints
        ]
        if not all(validation_checks):
            continue

        next_variable = get_next_unassigned_variable(schedule)
        if not next_variable:
            return schedule  # We have a winner!

        possible_values = get_possible_values(schedule, next_variable)
        queue.extendleft(
            reversed([{**schedule, next_variable: value} for value in possible_values])
        )

    return {}  # No solution found


def find_schedule(
    activities: List[Activity],
    slots: List[RoomSlot],
    progress_callback: Callable[[deque], None] = None,
) -> Schedule:
    """ Finds a schedule that meets all constraints
        Returns map between Activity and RoomSlots, or empty dict if not possible
    """
    if len(activities) > len(slots):
        raise SchedulerError("Number of activities exceeds slots")

    # schedule = all_combination_scheduler(activities, slots, constraints)
    schedule = search_scheduler(activities, slots, progress_callback)
    return schedule
