from scheduler import Activity, RoomSlot, find_schedule


def test_find_schedule_no_constraints():
    """ Given a set of Activities, RoomSlots 
        and no constrains, calling find_schedule
        should be able to find mapping for all Activities
    """
    activities = ["A1", "A2", "A3"]
    slots = [("R1", "M8"), ("R1", "M9"), ("R2", "M8"), ("R2", "M9")]

    schedule = find_schedule(activities, slots)

    assert len(schedule) == 3

    assert set(schedule.keys()) == set(activities), "all activities should be mapped"

    solution_slots = schedule.values()
    assert set(solution_slots) < set(slots), "all values should be from original slots"

    assert len(set(solution_slots)) == len(
        solution_slots
    ), "slots in solution must be unique"
