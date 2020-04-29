import pytest  # type: ignore

from scheduler import find_schedule, SchedulerError


def check_basic_properties_of_schedule(activities, slots, schedule):
    " Verify the invariants of the correct schedule "
    assert len(schedule) == 3

    assert set(schedule.keys()) == set(activities), "all activities should be mapped"

    solution_slots = schedule.values()
    assert set(solution_slots) < set(slots), "all values should be from original slots"

    assert len(set(solution_slots)) == len(
        solution_slots
    ), "slots in solution must be unique"


def test_find_schedule_no_constraints():
    """ Given a set of Activities, RoomSlots
        and no constrains, calling find_schedule
        should be able to find mapping for all Activities
    """
    activities = ["A1", "A2", "A3"]
    slots = [("R1", "M8"), ("R1", "M9"), ("R2", "M8"), ("R2", "M9")]

    schedule = find_schedule(activities, slots)

    check_basic_properties_of_schedule(activities, slots, schedule)


def test_find_schedule_not_enough_slots():
    """ Given a set of Activities and to few RoomSlots
        calling find_schedule
        should raise exception
    """
    activities = ["A1", "A2"]
    slots = [("R1", "M8")]

    with pytest.raises(SchedulerError):
        find_schedule(activities, slots)


def test_find_schedule_single_constraint():
    """ given a set of Activities and RoomSlots
        and a constraint function that check if given activity
        is placed in exact room, we should get a solution
        that schedules that activity into that room
    """
    activities = ["A1", "A2", "A3"]
    slots = [("R1", "M8"), ("R1", "M9"), ("R2", "M8"), ("R2", "M9")]

    def a2_constraint(schedule):
        for activity, slot in schedule.items():
            if activity == "A2" and slot[0] != "R2":
                return False
        return True

    schedule = find_schedule(activities, slots, [a2_constraint])
    check_basic_properties_of_schedule(activities, slots, schedule)

    # check if constraint is met on the result schedule
    print(f"{schedule=}")
    assert a2_constraint(schedule), "schedule should match given constraints"
