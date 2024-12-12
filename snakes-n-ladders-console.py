from threading import Thread, Timer
from random import randint
from timeit import Timer
import timeit, time, numpy
# from numpy.random import randint

NUM_ITERATIONS = 1000
ONLY_WIN_ON_EXACT = True
ALL_LADDERS_ARE_SNAKES = True

# now = Timer
now = time.time()
turns_to_win = []
turns = []
positions = []

NUM_FIELDS = 100

jumps_dict = {
    2: 38,
    7: 14,
    8: 31,
    15: 26,
    16: 6,
    21: 42,
    28: 84,
    36: 44,
    46: 25,
    49: 11,
    51: 67,
    62: 19,
    64: 60,
    71: 91,
    74: 53,
    78: 98,
    87: 94,
    92: 88,
    95: 75,
    99: 80,
}

if ALL_LADDERS_ARE_SNAKES:
    jumps_dict: dict[int, int] = {sorted(entry, reverse=True)[0]:sorted(entry, reverse=True)[1] for entry in jumps_dict.items()}


#prev ~33sec
#after jumps_dict ~20sec

if ONLY_WIN_ON_EXACT:
    def set_position(position:int):
        pos = NUM_FIELDS - position % NUM_FIELDS if position//NUM_FIELDS else position
        return jumps_dict.get(pos, pos)
else:
    def set_position(position:int):
        pos = min(position, NUM_FIELDS)
        return jumps_dict.get(pos, pos)

    
def set_position_inline(position: int):
    pos = NUM_FIELDS - position % NUM_FIELDS if position//NUM_FIELDS else position
    return jumps_dict.get(pos, pos)

def set_position_inline_twice(position: int):
    return jumps_dict.get(NUM_FIELDS - position % NUM_FIELDS if position // NUM_FIELDS else position, NUM_FIELDS - position % NUM_FIELDS if position // NUM_FIELDS else position)

def roll_dice():
    return randint(1, 6)

def play():
    turn = 0
    player_pos = 1
    t = []
    while player_pos < NUM_FIELDS:
        turn +=1
        roll = roll_dice()
        player_pos = set_position(player_pos + roll)
        player_pos= jumps_dict.get(player_pos, player_pos)
                
        t.append(player_pos)
    assert player_pos == NUM_FIELDS
    if len(t) < 40 or len(t) >15000:
        turns.append(t)
    turns_to_win.append(turn)
    turns_to_win.append(turn)

def main():
    
    # threads = [Thread(target=play) for i in range(NUM_ITERATIONS)]
    # for t in threads:
    #     t.start()


    # for t in threads:
    #     t.join()
    for i in range(NUM_ITERATIONS):
        play()
    
    
    print(f"all done in: {round(time.time()-now, 2)}s")
    print(f"it took an average of {sum(turns_to_win) / len(turns_to_win)} turns to win")
    
    print(f"slowest was {max(*turns_to_win)} turns")
    print(f"fastest was {min(*turns_to_win)} turns")
    print("\nfastest turnorder was:")
    p = False
    for t in turns:
        if len(t) == min(*turns_to_win):
            print(t)
            p=True
    if not p:
        print("not recorded")

    print("\nlongest ending was:")
    p = False
    for t in turns:
        if len(t) == max(*turns_to_win):
            print(t[-20:])
            p=True
    if not p:
        print("not recorded")

    print("recorded turn lengths")
    print(sorted([len(t) for t in turns]))


    npArr = numpy.array(positions)
    print(f"hist positions: {numpy.histogram(npArr)}")
    print(f"cumsum positions: {npArr.cumsum()}")
    print(f"cumprod positions: {npArr.cumprod()}")


if __name__ == "__main__":
    main()
# import timeit
# import numpy

# setup = "i = {}"
# stmt = """
# for x in range(i):
#     3 + 3
# """
# import timeit, numpy



# t1 = timeit.Timer(lambda: set_position_inline_twice(20))
# t2 = timeit.Timer(lambda: set_position_inline(20))

# print(t1)
# print(t2)