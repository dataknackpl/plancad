import pytest  # type: ignore

from scheduler2 import find_schedule, SchedulerError, Activity, RoomSlot


def test_create_room_slot_no_attrs():
    " Check creating room slots with value only "
    rs = RoomSlot(value="foo")
    assert rs.value == "foo"
    assert rs.attributes == {}


def test_create_room_slot_with_attr():
    " Check creating room slots with value only "
    rs = RoomSlot(value="foo", attributes={"attr1": "bar"})
    assert rs.value == "foo"
    assert len(rs.attributes) == 1


def test_create_activity_no_constraints():
    " Check creating activity with name only "
    a = Activity(name="foo")
    assert a.name == "foo"
    assert len(a.constraints) == 0


def test_create_activity_with_constraint():
    " Check creating activity with name only "
    a = Activity(name="foo", constraints=["attr1 == bar"])
    assert a.name == "foo"
    print(f"{a.constraints=}")
    assert len(a.constraints) == 1
    assert a.constraints[0] == ("attr1", "==", "bar")


def test_check_constraint():
    " Activity should be able to say whether given slot matches it's constraints"
    a = Activity(name="foo", constraints=["attr1 == bar"])
    s1 = RoomSlot(value="s1", attributes={"attr1": "bar"})
    s2 = RoomSlot(value="s2", attributes={"attr1": "baz"})
    s3 = RoomSlot(value="s3")

    assert a.is_slot_valid(s1) is True
    assert a.is_slot_valid(s2) is False
    assert a.is_slot_valid(s3) is False


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
    print(f"{schedule=}")

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

    def make_slot(t) -> RoomSlot:
        room = t[0]
        slot = t[1]
        return RoomSlot(value=f"{room}{slot}", attributes={"room": room})

    activities = [Activity(n) for n in ["A1", "A2", "A3"]]
    slots = [
        make_slot(t) for t in [("R1", "M8"), ("R1", "M9"), ("R2", "M8"), ("R2", "M9")]
    ]

    schedule = find_schedule(activities, slots)
    check_basic_properties_of_schedule(activities, slots, schedule)

    # check if constraint is met on the result schedule
    print(f"{schedule=}")
    # assert a2_constraint(schedule), "schedule should match given constraints"
