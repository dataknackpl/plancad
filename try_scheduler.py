from tqdm import tqdm
import time  # NOQA

from scheduler import (
    total_number_of_combinations,
    find_schedule,
    Activity,
    RoomSlot,
)


def make_slot(t) -> RoomSlot:
    room = t[0]
    slot = t[1]
    return RoomSlot(value=f"{room}{slot}", attributes={"room": room})


SIZE = 9

# activities = [Activity(n, [f"room == R{SIZE-int(n[1:])}"])
#               for n in [f"A{i}" for i in range(SIZE)]]
activities = [Activity(n) for n in [f"A{i}" for i in range(SIZE)]]
activities = activities + [Activity("AX", [f"room == R0"])]
activities = activities + [Activity("AY", [f"room == R{SIZE}"])]

slots = [make_slot(t) for t in [(f"R{i}", "M8") for i in range(len(activities))]]
total_combinations = total_number_of_combinations(len(slots), len(activities))
print(f"{total_combinations=}")
pbar = tqdm(total=total_combinations, initial=0)
# prev_combinations = total_combinations


def debug_progress_callback(queue):
    # global prev_combinations
    # remaining_combinations = sum([
    #    total_number_of_combinations(len(slots)-len(elem), len(activities)-len(elem))
    #    for elem in queue
    # ])
    # pbar.update(prev_combinations-remaining_combinations)
    pbar.update(1)
    # print(len(queue))
    # print(queue)
    # prev_combinations = remaining_combinations
    # time.sleep(0.1)


schedule = find_schedule(activities, slots, progress_callback=debug_progress_callback)
# schedule = find_schedule(activities, slots)
pbar.close()
print(schedule)
